from datasets import Dataset
import datasets
import subprocess
import os

# internal imports
from compiler_fuzzing.utils.logs import record_case
from compiler_fuzzing.utils.files import valid_path
from compiler_fuzzing.utils import (
    display,
    files,
)

def check_syntax_string(code, config):
    root_path = config["root_path"]
    files.create_path(f"{root_path}/files/temp/")
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
        

def check_syntax_file(playbook_path, inventory_path):
    
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

def check_ansible_syntax_module(sample_data, yaml_base_path, inventory_path):
    playbook_path = f"{yaml_base_path}/{sample_data['level']}/{sample_data['name']}"
    
    if not valid_path(playbook_path):
        return 0
    files_and_dirs = os.listdir(playbook_path)

    # Filter out directories
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(playbook_path, f))]
    
    flag = 0
    
    for f in files:
           
        try:
            check_syntax_file(os.path.join(playbook_path, f), inventory_path)
            flag = 1
        except Exception as e:
            flag += 0
    
    return flag

    
    
    

def check_ansible_syntax(sample_data, yaml_base_path, inventory_path, num_digits=5):
    level = sample_data["level"]
    issue_id = sample_data["id"]
    playbook_path = f"{yaml_base_path}/lv{level}/{int(issue_id):0{num_digits}}.yaml"
    if not valid_path(playbook_path):
        return 0

    try:
        # Check the syntax of the playbook
        check_syntax_file(playbook_path, inventory_path)
        
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
    task = args.task
    if task == 'module':
        base_dir = config['module_output_dir']
        num_digits = 5
    elif task == 'github_issue':
        base_dir = config['output_dir']
        num_digits = len(str(max(ds['id'])))
    if args.timestamp is not None:
        base_path = f"{base_dir}/{args.timestamp}"
    else:
        file_list = files.list(base_dir)
        if 'debug' in file_list : file_list.pop(file_list.index('debug'))
        if len(file_list) == 0:
            raise FileNotFoundError(
                'No directories in target location. Need to generate ansible files first.'
            )
        src_dir = sorted(file_list)[-1]
        base_path = f'{base_dir}/' + src_dir

    file_path = f"{base_path}/manifest_ds.csv"
    datasets.disable_caching()
    ds = Dataset.from_csv(file_path)
    inventory_path = config["inventory_file"]
    
    def mapper_fn(sample):
        if task == 'module':
            syntax = check_ansible_syntax_module(sample, base_path, inventory_path)
        elif task == 'github_issue':
            syntax = check_ansible_syntax(sample, base_path, inventory_path, num_digits)
        
        sample.update({
            'syntax' : syntax
        })
        return sample
    
    output_ds = ds.map(mapper_fn)
    
    trgt_path = file_path
    display.green(f'\nsaving data to {trgt_path} ...')
    output_ds.to_csv(trgt_path)
    
