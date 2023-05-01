from ..utils import get_config, get_response, get_yaml_data, remove_tilda, check_ansible_syntax
from compilier_fuzzing.utils.log_utils import *
from tqdm import tqdm
import pandas as pd
import argparse

def get_prompts(df, prompt):
    df['prompt'] = prompt + df['TITLE']
    return df

def get_dataframe(path, generation_limit=10, logger=None, prompt="", config=None):
    df = pd.read_excel(path)
    
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
                resp = get_response(df.iloc[ind]['prompt'], config=config)
                response = resp['choices'][0]['message']['content']
                logger.info(f"response: {response}")
                column_index = df.columns.get_loc('response')
                df.iloc[ind, column_index] = response
                pbar.update(1)
                count += 1
    
    print("Number of playbooks created:", (df.response != '').sum())           
    return df
    

def get_valid_annotation(df):
    df['code'] =df['response'].apply(remove_tilda)
    df['valid_yaml'] = df['code'].apply(get_yaml_data)
    # df['valid_syntax'] = df['code'].apply(check_ansible_syntax)
    print(df['valid_yaml'].sum(), df['valid_syntax'].sum())
    return df


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="compilier_fuzzing/confs/config.yaml")
    args = parser.parse_args()

    config = get_config(name=args.config)

    dummy_prompt = config["dummy_prompt"]
    github_data_path = config["github_issue_path"]
    github_issue_file_name = config['github_issue_file_name']
    
    logger, handler = get_log_files(config=config)
    excel_path = f"{github_data_path}/{github_issue_file_name}"
    df = get_dataframe(excel_path, generation_limit=5, logger=logger, prompt=dummy_prompt, config=config)

    df = get_valid_annotation(df)

    df.to_feather(f'{github_data_path}/chatgpt_github_yaml.feather', index=False)

    df.to_csv(f'{github_data_path}/chatgpt_github_yaml.csv', index=False)



            


