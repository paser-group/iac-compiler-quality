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

def subprocess_ansible(sample_data, yaml_base_path, inventory_path):
    level = sample_data["level"]
    issue_id = sample_data["ID"]
    playbook_path = f"{yaml_base_path}/lv{level}/{issue_id}.yaml"
    if not valid_path(playbook_path):
        return 0
    output = ""
    try:
        # Check the syntax of the playbook
        ansible_command = ["ansible-playbook", playbook_path, "-i", inventory_path]

        output = subprocess.run(
            ansible_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        display.green(
            "Ansible has run successfully: ", 
            playbook_path
        )
        record_case(
            success=True,
            tag="run",
            **{
                "issue id": sample_data["ID"],
                "issue title": sample_data["TITLE"], 
                "issue prompt": sample_data["prompt"],
                "issue Output": output
            }
        )
        
        return output.stdout
    except Exception as e:
        # logger.error(f"issue id: {issue_id}, issue title: {issue_title}, reason: Invalid syntax., issue prompt: {issue_prompt}")
        record_case(
            success=False, 
            **{
                "issue id": sample_data["ID"],
                "issue title": sample_data["TITLE"], 
                "reason": f"{e}", 
                "issue prompt": sample_data["prompt"]
            }
        )
        return output if output == "" else output.stdout
    
    
def run_ansible(args, config):
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
    inventory = config["inventory_file"]
    
    def mapper_fn(sample):
        if sample["syntax"] == 0:
            ansible_output = None
        else:
            ansible_output = subprocess_ansible(sample, base_path, inventory)
        
        sample.update({
            'output' : ansible_output
        })
        
        return sample
    
    output_ds = ds.map(mapper_fn)
    
    trgt_path = file_path
    display.green(f'\nsaving data to {trgt_path} ...')
    output_ds.to_csv(trgt_path)