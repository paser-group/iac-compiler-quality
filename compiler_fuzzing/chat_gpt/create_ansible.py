"""
this code is used to prompt chatgpt to create ansible playbooks
"""
# external imports
from tqdm import tqdm
import pandas as pd
from datasets import Dataset

# internal imports
from compiler_fuzzing.utils import ChatSession, yaml, logs
from compiler_fuzzing import utils, arguments
from .prompt_engg import PromptEngg


def get_valid_annotation(df):
    df['code'] =df['response'].apply(utils.strings.remove_tilde)
    # df['code'].apply(save_to_file)
    df['valid_yaml'] = df['code'].apply(yaml.get_yaml_data)
    df['valid_syntax'] = df['code'].apply(yaml.check_ansible_syntax)
    print(df['valid_yaml'].sum(), df['valid_syntax'].sum())
    return df


def create_ansible(args):
    """
    this function is used to create ansible files by 
    """

    utils.display.title('Generating Ansible Playbooks With ChatGPT')
    # read in config data
    config = utils.files.load_yaml(args.config)

    # initialize logging
    #logger, handler = logs.get_log_files(config=config)

    dummy_prompt, github_data_path, github_issue_file_name = (
        config["dummy_prompt"],
        config["github_issue_path"],
        config["github_issue_file_name"],
    )


    # read in excel data as huggingface dataset
    excel_path = f"{github_data_path}/{github_issue_file_name}"
    ds = Dataset.from_pandas(
        (df := pd.read_excel(excel_path)),
        preserve_index=True
    )

    # load dataset

    ##################################
    # TODO
    #
    # 1) insantiate prompt generator
    #                               
    # 2) generate prompts from data
    ##################################

    # TODO populate configs so that this doesn't error out
    # generators = [PromptEngg(config, lvl, ds) for lvl in range(6)]
    breakpoint()
    generators = [PromptEngg(config, lvl, ds) for lvl in range(1, 6)]
    # ds = generator(ds)

    ##################################
    breakpoint()

    # TODO delete this
    sys_msg = "You are a helpful assistant who will generate syntactically correct Ansible YAML Playbook for testing purposes. Do not include any explanation or context or introduction statement. Make sure to include ``` before and after Ansible code to denote the YAML section"
    limit = 1
    response = []
    for i, sample in enumerate(tqdm( ds, desc='generating playbooks', total=len(ds))):
        if i == limit : break
        # TODO replace with response  generation code
        prompt = dummy_prompt + sample['TITLE']

        session = ChatSession(
            config['openai']['key'],
            config["openai"]["organization"],
            system_msg=sys_msg
        )
        response.append(session(prompt))
        #logger.info(f"response: {response[-1]}")
        
    # truncate dataset to accomodate amount of responses generated
    output_ds = ds.select(range(len(response)))

    # TODO implement validation code
    # validations = get_valid_annotation(response)
    # output_ds.add_column('VALIDITY', validations)

    # append columns to dataset
    output_ds = output_ds.add_column('RESPONSE', response)
    output_dir = f'{github_data_path}/chatgpt_github_yaml-{utils.strings.now()}.csv'
    utils.display.green(f'saving data to {output_dir}...')
    output_ds.to_csv(output_dir)

    
    utils.display.green(f'\n\nGenerated {len(output_ds)} Ansible Playbook(s)', end='\n\n')
    utils.display.title('Finished Playbook Generation')
    breakpoint()
    #ds.to_csv(f'results{utils.now()}.csv')

