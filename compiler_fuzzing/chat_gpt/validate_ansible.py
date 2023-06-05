from datasets import Dataset
import datasets
import subprocess


# internal imports
from compiler_fuzzing.utils.logs import record_case
from compiler_fuzzing.utils.files import valid_path
from compiler_fuzzing.utils import (
    display,
    files,
)

def check_syntax_string(code, config):
    root_path = config["root_path"]
    temp_yaml_path = f"{root_path}/files/temp/tmp.yaml"
    files.write_file(temp_yaml_path, code)
    inventory_path = config["inventory_file"]
    
    try:
        
        subprocess.check_output(
            [
                'ansible-playbook',
                temp_yaml_path,
                '--syntax-check',
                "-i", 
                inventory_path
            ],
            stderr=subprocess.STDOUT
        )
        
        record_case(
            success=True, 
            **{
                "result": f"Ansible syntax check passed for playbook: {temp_yaml_path}"
            }
        )
        return 1
    except Exception as e:
        # logger.error(f"issue id: {issue_id}, issue title: {issue_title}, reason: Invalid syntax., issue prompt: {issue_prompt}")
        
        return 0
        

def check_ansible_syntax(sample_data, yaml_base_path, inventory_path):
    level = sample_data["level"]
    issue_id = sample_data["id"]
    playbook_path = f"{yaml_base_path}/lv{level}/{issue_id}.yaml"
    if not valid_path(playbook_path):
        return 0

    try:
        # Check the syntax of the playbook
        subprocess.check_output(
            [
                'ansible-playbook',
                playbook_path,
                '--syntax-check',
                "-i", 
                inventory_path
            ],
            stderr=subprocess.STDOUT
        )
        
        # display.green(
        #     f"Ansible syntax check passed for playbook: {playbook_path}"            
        # )
        
        record_case(
            success=True, 
            **{
                "issue id": sample_data["id"],
                "issue title": sample_data["title"], 
                "result": f"Ansible syntax check passed for playbook: {playbook_path}", 
                "issue prompt": sample_data["prompt"]
            }
        )
        return 1
    except Exception as e:
        # logger.error(f"issue id: {issue_id}, issue title: {issue_title}, reason: Invalid syntax., issue prompt: {issue_prompt}")
        record_case(
            success=False, 
            **{
                "issue id": sample_data["id"],
                "issue title": sample_data["title"], 
                "reason": f"{e}", 
                "issue prompt": sample_data["prompt"]
            }
        )
        return 0



def validate_ansible(args, config):
    if args.timestamp is not None:
        base_path = f"{config['output_dir']}/{args.timestamp}"
    else:
        file_list = files.list(config['output_dir'])
        if 'debug' in file_list : file_list.pop(file_list.index('debug'))
        if len(file_list) == 0:
            raise FileNotFoundError(
                'No directories in target location. Need to generate ansible files first.'
            )
        src_dir = sorted(file_list)[-1]
        base_path = f'{config["output_dir"]}/' + src_dir

    file_path = f"{base_path}/manifest_ds.csv"
    datasets.disable_caching()
    ds = Dataset.from_csv(file_path)
    inventory_path = config["inventory_file"]
    
    def mapper_fn(sample):
        sample.update({
            'syntax' : check_ansible_syntax(sample, base_path, inventory_path)
        })
        return sample
    
    output_ds = ds.map(mapper_fn)
    
    trgt_path = file_path
    display.green(f'\nsaving data to {trgt_path} ...')
    output_ds.to_csv(trgt_path)
    
