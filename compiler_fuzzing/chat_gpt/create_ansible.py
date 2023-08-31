"""
this code is used to prompt chatgpt to create ansible playbooks
"""
# external imports
import sys
import pandas as pd
import datasets
import requests
import re
from tqdm import tqdm
from datasets import Dataset

# internal imports
from .prompt_engg import PromptEngg
from .validate_ansible import check_syntax_string
from compiler_fuzzing.utils import (
    ChatSession,
    yaml,
    logs,
    files,
    display,
    strings,
)


def _unused_code():
    """
    might need these later
    """
    
    # initialize logging
    #logger, handler = logs.get_log_files(config=config)
    #logger.info(f"response: {response[-1]}")
    pass

def generate_manifest_ds(args, config, ds, level_list):
    
    # build generators and get updated dataset
    prompt_method = args.prompt_method
    generators = [PromptEngg(config, lvl, ds, prompt_method=prompt_method) for lvl in level_list]
    ds = datasets.interleave_datasets(
        [gen.get_updated_dataset() for gen in generators]
    )

    response = []
    second_query = []
    for i, sample in enumerate(tqdm(ds, desc='collecting chatgpt responses', total=len(ds))):
        if i == args.limit : break

        session = ChatSession(
            config['openai']['key'],
            config["openai"]["organization"],
            system_msg=sample['sys_role']
        )
        try:
            reply = session.get_response(sample['prompt'])
            code = strings.remove_tilde(reply) \
                if '```' in reply \
                else ''
            
            correct_syntax = check_syntax_string(code, config)
            second_call = 0
            if not correct_syntax:
                second_call = 1
                reply = session.get_response(config["syntax_nudge"])
            
                
            second_query.append(second_call)
            response.append(reply)
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            sys.exit(0)
        except Exception as e:
            
            display.red(f'timeout error on sample {i}')
            response.append('TIMEOUT ERROR')
            second_query.append(0)

    # truncate dataset to accomodate amount of responses generated
    output_ds = ds.select(range(len(response)))
    assert len(response) == len(second_query)
    
    # append columns to dataset
    output_ds = output_ds.add_column('response', response)
    output_ds = output_ds.add_column('second_query', second_query)

    # extract code from the responses and add to a new column
    def mapper_fn(sample):
        # extract code from response
        sample.update({
            'code' : \
                strings.remove_tilde(sample['response']) \
                if '```' in sample['response'] \
                else '',
        })

        # check for yaml header and remove if it exists
        code = sample['code'].strip()
        if re.match(r'^yaml', code) is not None:
            code = code[4:].strip()
            sample['code'] = code

        return sample
    output_ds = output_ds.map(mapper_fn)
    
    return output_ds

def generate_playbooks(level_list, output_ds, config, base_output_path):
    # generate YAML files with dataset
    display.green(f'\ngenerating YAML files to {base_output_path}...')
    num_digits = len(str(max(output_ds['id'])))

    # get directories for each level
    output_lv_paths = [
        f'{base_output_path}/lv{lv}'
        for lv in level_list
    ]
    for pth in output_lv_paths : files.create_path(pth)

    # write files to output directory
    for i, sample in enumerate(tqdm(output_ds, desc='generating playbooks', total=len(output_ds))):
        if sample['code'] != '':
            files.write_file(
                output_lv_paths[level_list.index(sample['level'])]+ \
                    f'/{int(sample["id"]):0{num_digits}}.yaml',
                sample['code']
            )

def get_response(token, url): 
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        display.warning(f'got status code {response.status_code}')
        data = None 
    return data

def preprocess_dataset(dataset, config, limit):
    dataset = dataset.rename_column('TITLE', 'title')
    dataset = dataset.rename_column('ID', 'id')
    repo_owner = config['github']['repo_owner']
    repo_name = config['github']['repo_name']
    token = config['github']['token']
    
    if limit > 0:
        dataset = dataset.select(range(limit))
    
    def mapper_fn(sample):
        issue_id = sample['id']
        issue_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_id}"
        
        issue = get_response(token=token, url=issue_url)
        issue_body = issue['body']
        comment_url = issue['comments_url']
        comments = get_response(token=token, url=comment_url)
        comment_bodies = [comment['body'] for comment in comments]
        sample.update({
            'body' : issue_body,
            'comments' : comment_bodies
        })
        
        return sample
    
    ds = dataset.map(mapper_fn)
    
    return ds
    
    

def create_ansible(args, config):
    """
    this function is used to create ansible files by making API calls to ChatGPT
    """
    # read in excel data as huggingface dataset

    trgt_file = config['data_path']
    datasets.disable_caching()
    if trgt_file.endswith('.xlsx'):
        ds = Dataset.from_pandas(
            pd.read_excel(trgt_file)
        )
    else:
        ds = Dataset.from_csv(trgt_file)

    display.title('Pre-Processing Dataset: Get issue body and comments')
    
    if args.limit > 0:
        ds = ds.select(range(args.limit))

    ds = preprocess_dataset(ds, config, args.limit)
    display.title('Generating Ansible Playbooks With ChatGPT')
    # get number of levels for prompt engineering.
    level_list = [int(x) for x in config["levels"].split(",")]
    args.limit = args.limit * len(level_list)
    num_levels = len(level_list)
    # num_levels = files.count_files_in(
    #     config['taxonomy_filepath'],
    #     match_str='.yaml'
    # )

    # build the dataset of manifests
    output_ds = generate_manifest_ds(args, config, ds, level_list)

    # build output path string
    timestamp = strings.now()
    if not args.debug: 
        base_output_path = \
            config['output_dir'] + \
            f'/{timestamp}'
    else:
        base_output_path = f'{config["output_dir"]}/debug'
    files.create_path(base_output_path)

    trgt_path = base_output_path + '/manifest_ds.csv'
    display.green(f'\nsaving data to {trgt_path} ...')
    output_ds.to_csv(trgt_path)

    # generate output configs
    generate_playbooks(level_list, output_ds, config, base_output_path)

    # display status messages
    num_blanks = output_ds[:]['code'].count('')
    display.green(
        f'\n\nGenerated {len(output_ds) - num_blanks} Ansible Playbook(s) out of {len(output_ds)}\n' + \
            f'{num_blanks} example(s) generated no code', 
        end='\n\n'
    )
    display.title('Finished Playbook Generation')

    # cleanup cache
    ds.cleanup_cache_files()
    if args.debug : breakpoint()
