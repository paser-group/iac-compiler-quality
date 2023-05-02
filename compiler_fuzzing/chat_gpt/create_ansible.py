"""
this code is used to prompt chatgpt to create ansible playbooks
"""

# external imports
from tqdm import tqdm
import pandas as pd
import argparse
from datasets import Dataset

# internal imports
from compiler_fuzzing.utils.yaml import get_yaml_data, check_ansible_syntax
from compiler_fuzzing.utils import ChatHandler
from compiler_fuzzing import utils, arguments


def get_prompts(df, prompt):
    df['prompt'] = prompt + df['TITLE']
    return df

def collect_responses(path, generation_limit=10, logger=None, prompt="", config=None):
    df = pd.read_excel(path)
    #ds = Dataset.from_pandas(df)
    
    df = get_prompts(df, prompt=prompt)
    df['response'] = ''
    df = df[:generation_limit]

    count = 0
    list_of_responses = []
    
    with tqdm(total=None, desc="Generating playbooks") as pbar:
        for ind in df.index:
            if count >= generation_limit:
                break
            if df.iloc[ind]['response'] == '':
                handler = ChatHandler(
                    config['openai']['key'],
                    config["openai"]["organization"],
                    system_msg="You are a helpful assistant who will generate syntactically correct Ansible YAML Playbook for testing purposes. Do not include any explanation or context or introduction statement. Make sure to include ``` before and after Ansible code to denote the YAML section"
                )
                response = handler.get_response(df.iloc[ind]['prompt'])
                logger.info(f"response: {response}")
                column_index = df.columns.get_loc('response')
                df.iloc[ind, column_index] = response
                pbar.update(1)
                count += 1
    
    print("Number of playbooks created:", (df.response != '').sum())           
    return df
    

def get_valid_annotation(df):
    df['code'] =df['response'].apply(utils.strings.remove_tilde)
    # df['code'].apply(save_to_file)
    df['valid_yaml'] = df['code'].apply(get_yaml_data)
    df['valid_syntax'] = df['code'].apply(check_ansible_syntax)
    print(df['valid_yaml'].sum(), df['valid_syntax'].sum())
    return df


def main():
    """
    this function is used to create ansible files by 
    """

    # read in config data
    args = arguments.parse()
    config = utils.files.load_yaml(args.config)
    dummy_prompt, github_data_path, github_issue_file_name = (
        config["dummy_prompt"],
        config["github_issue_path"],
        config["github_issue_file_name"],
    )

    # read in excel data as huggingface dataset
    excel_path = f"{github_data_path}/{github_issue_file_name}"
    ds = Dataset.from_pandas(
        pd.read_excel(excel_path)
    )

    # load dataset

    ##################################
    # TODO
    #
    # 1) insantiate prompt generator
    #                               
    # 2) generate prompts from data
    ##################################

    generator = None
    # ds = generator(ds)

    ##################################
    
    """
    prog_bar = tqdm(
        range(len(ds)),
        desc = 'collecting responses'
    )
    results = []
    for sample in tqdm(ds, desc='generating playbooks'):
        pass

    output_ds = Dataset.from_list(results)
    output_ds.to_csv(f'results{utils.now()}.csv')
    """

    # generate YAML files from ChatGPT
    logger, handler = utils.logs.get_log_files(config)
    df = collect_responses(
        excel_path,
        generation_limit=1,
        logger=logger,
        prompt=dummy_prompt,
        config=config
    )

    df = get_valid_annotation(df)

    # save to file
    df.to_feather(f'{github_data_path}/chatgpt_github_yaml.feather', index=False)
    df.to_csv(f'{github_data_path}/chatgpt_github_yaml.csv', index=False)

