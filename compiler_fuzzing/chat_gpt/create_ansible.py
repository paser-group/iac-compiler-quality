"""
this code is used to prompt chatgpt to create ansible playbooks
"""
# external imports
import sys
import pandas as pd
import datasets
from tqdm import tqdm
from datasets import Dataset

# internal imports
from .prompt_engg import PromptEngg
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

def generate_manifest_ds(args, config, ds, num_levels):

    # build generators and get updated dataset
    generators = [PromptEngg(config, lvl, ds) for lvl in range(num_levels)]
    ds = datasets.interleave_datasets(
        [gen.get_updated_dataset() for gen in generators]
    )

    response = []

    # truncate dataset if limit argument is specified
    if args.limit > 0:
        ds = ds.select(range(args.limit))

    # 
    for i, sample in enumerate(tqdm(ds, desc='collecting chatgpt responses', total=len(ds))):
        if i == args.limit : break

        session = ChatSession(
            config['openai']['key'],
            config["openai"]["organization"],
            system_msg=sample['sys_role']
        )
        try:
            response.append(
                session.get_response(sample['prompt'])
            )
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            sys.exit(0)
        except Exception:
            display.red(f'timeout error on sample {i}')
            response.append('TIMEOUT ERROR')

    # truncate dataset to accomodate amount of responses generated
    output_ds = ds.select(range(len(response)))

    # append columns to dataset
    output_ds = output_ds.add_column('response', response)

    # extract code from the responses and add to a new column
    def mapper_fn(sample):
        sample.update({
            'code' : \
                strings.remove_tilde(sample['response']) \
                if '```' in sample['response'] \
                else '',
        })
        return sample
    output_ds = output_ds.map(mapper_fn)
    
    return output_ds

def generate_playbooks(num_levels, output_ds, config, base_output_path):
    # generate YAML files with dataset
    display.green(f'\ngenerating YAML files to {base_output_path}...')
    num_digits = len(str(max(output_ds['ID'])))

    # get directories for each level
    output_lv_paths = [
        f'{base_output_path}/lv{lv}'
        for lv in range(num_levels)
    ]
    for pth in output_lv_paths : files.create_path(pth)

    # write files to output directory
    for i, sample in enumerate(tqdm(output_ds, desc='generating playbooks', total=len(output_ds))):
        if sample['code'] != '':
            files.write_file(
                output_lv_paths[sample['level']]+ \
                    f'/{int(sample["ID"]):0{num_digits}}.yaml',
                sample['code']
            )

def create_ansible(args, config):
    """
    this function is used to create ansible files by 
    """

    display.title('Generating Ansible Playbooks With ChatGPT')

    # read in excel data as huggingface dataset
    ds = Dataset.from_pandas(
        pd.read_excel(config['data_path'])
    )

    # count number of config files
    num_levels = files.count_files_in(
        config['taxonomy_filepath'],
        match_str='.yaml'
    )

    # build the dataset of manifests
    output_ds = generate_manifest_ds(args, config, ds, num_levels)

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
    generate_playbooks(num_levels, output_ds, config, base_output_path)

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
