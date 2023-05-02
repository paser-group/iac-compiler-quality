"""
this code is used to prompt chatgpt to create ansible playbooks
"""
# external imports
from tqdm import tqdm
import pandas as pd
from datasets import Dataset
import datasets

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


def get_valid_annotation(df):
    df['code'] =df['response'].apply(strings.remove_tilde)
    # df['code'].apply(save_to_file)
    df['valid_yaml'] = df['code'].apply(yaml.get_yaml_data)
    df['valid_syntax'] = df['code'].apply(yaml.check_ansible_syntax)
    print(df['valid_yaml'].sum(), df['valid_syntax'].sum())
    return df


def create_ansible(args, config):
    """
    this function is used to create ansible files by 
    """

    display.title('Generating Ansible Playbooks With ChatGPT')

    # initialize logging
    #logger, handler = logs.get_log_files(config=config)

    dummy_prompt, data_path = (
        config["dummy_prompt"],
        config["data_path"],
    )


    # read in excel data as huggingface dataset
    ds = Dataset.from_pandas(
        pd.read_excel(data_path)
    )


    # build generators and get updated dataset
    num_levels = 6
    generators = [PromptEngg(config, lvl, ds) for lvl in range(num_levels)]
    ds = datasets.interleave_datasets(
        [gen.get_updated_dataset() for gen in generators]
    )

    #limit = 1
    limit = num_levels
    response = []
    for i, sample in enumerate(tqdm(ds, desc='generating playbooks', total=len(ds))):
        if i == limit : break

        session = ChatSession(
            config['openai']['key'],
            config["openai"]["organization"],
            system_msg=sample['sys_role']
        )
        response.append(
            session.get_response(sample['prompt'])
        )
        #logger.info(f"response: {response[-1]}")

    # truncate dataset to accomodate amount of responses generated
    output_ds = ds.select(range(len(response)))

    # TODO implement validation code
    # validations = get_valid_annotation(response)
    # output_ds.add_column('VALIDITY', validations)

    # append columns to dataset
    output_ds = output_ds.add_column('response', response)

    def mapper_fn(sample):
        sample.update({
            'code' : \
                strings.remove_tilde(sample['response']) \
                if '```' in sample['response'] \
                else '',
        })
            
        return sample
    output_ds = output_ds.map(mapper_fn)
    
    # get output path and save dataset
    source_dir, source_name = files.split_dir_fname(data_path)
    if args.debug : files.create_path(source_dir + '/debug')
    output_path = files.get_full_path(
        f'{source_dir}/' + 
        f'{source_name}-{strings.now()}.csv'
    )
    display.green(f'\nsaving data to {output_path}...')
    output_ds.to_csv(output_path)
    
    # display status messages
    display.green(f'\n\nGenerated {len(output_ds)} Ansible Playbook(s)', end='\n\n')
    display.title('Finished Playbook Generation')

    # cleanup cache
    ds.cleanup_cache_files()
    breakpoint()

