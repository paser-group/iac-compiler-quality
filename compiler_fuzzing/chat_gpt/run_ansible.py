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
    strings
)


def get_base_path(args, config):
    task = args.task
    if task == 'module':
        base_dir = config['module_output_dir']
    elif task == 'github_issue':
        base_dir = config['output_dir']
        
        
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
        
    return base_path

def create_docker_environment(docker_path, project_root_path):
    # Create New Docker Environment
        os.chdir(docker_path)
        docker_stop_command = ["docker", "compose", "stop"]
        docker_stop_log = subprocess.run(
            docker_stop_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        docker_up_command = ["docker", "compose", "up", "-d", "--force-recreate"]
        
        docker_up_log = subprocess.run(
            docker_up_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        docker_ps = ["docker", "ps"]
        docker_networks = ["docker", "network", "list"]
        
        docker_ps_log = subprocess.run(
            docker_ps,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        docker_networks_log = subprocess.run(
            docker_networks,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        record_case(
            success=True,
            tag="docker",
            **{
                "stop log": f"std err: {docker_stop_log.stderr}, std out: {docker_stop_log.stdout}",
                "up log": f"std err: {docker_up_log.stderr}, std out: {docker_up_log.stdout}", 
                "containers created": f"std err: {docker_ps_log.stderr}, std out: {docker_ps_log.stdout}",
                "network created": f"std err: {docker_networks_log.stderr}, std out: {docker_networks_log.stdout}",
                "timestamp": strings.now()
            }
        )
        
        os.chdir(project_root_path)


def run_ansible_playbook(playbook_path, inventory_path, private_key, become_password_file):
    
    ansible_command = [
        "ansible-playbook", playbook_path, 
        "-i", inventory_path, 
        "--private-key", private_key,
        "--become-password-file", become_password_file,
        "-vvv"
    ]
    
    output = subprocess.run(
        ansible_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=300,
        text=True
    )
    
    return output


def subprocess_ansible(sample_data, yaml_base_path, inventory_path, docker_path, private_key, become_password_file, num_digits=5):
    level = sample_data["level"]
    issue_id = sample_data["id"]
    playbook_path = f"{yaml_base_path}/lv{level}/{int(issue_id):0{num_digits}}.yaml"
    project_root_path = os.getcwd()
    if not valid_path(playbook_path):
        return 0
    output = ""
    try:
        
        create_docker_environment(docker_path, project_root_path)
        
        output = run_ansible_playbook(playbook_path, inventory_path, private_key, become_password_file)
        
        record_case(
            success=True,
            tag="run",
            **{
                "issue id": sample_data["id"],
                "issue title": sample_data["title"], 
                "issue prompt": sample_data["prompt"],
                "issue Output": f"std err: {output.stderr}, std out: {output.stdout}",
                "timestamp": strings.now()
            }
        )
        
        return output.stdout
    except Exception as e:
        # logger.error(f"issue id: {issue_id}, issue title: {issue_title}, reason: Invalid syntax., issue prompt: {issue_prompt}")
        record_case(
            success=False, 
            **{
                "issue id": sample_data["id"],
                "issue title": sample_data["title"], 
                "reason": f"{e}", 
                "issue prompt": sample_data["prompt"],
                "timestamp": strings.now()
            }
        )
        return output if output == "" else output.stdout

def subprocess_ansible_module(sample_data, yaml_base_path, inventory_path, docker_path, private_key, become_password_file):
    
    playbook_path = f"{yaml_base_path}/lv{sample_data['level']}/{sample_data['name']}"
    
    if not valid_path(playbook_path):
        return 0
    
    files_and_dirs = os.listdir(playbook_path)

    # Filter out directories
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(playbook_path, f))]
    
    project_root_path = os.getcwd()
    
    
    output = ""
    for f in files:
        output += f"\n\n{f}\n\n"
        try:
            playbook_path = os.path.join(playbook_path, f)
            create_docker_environment(docker_path, project_root_path)
            console_output = ""
            console_output = run_ansible_playbook(playbook_path, inventory_path, private_key, become_password_file)
            
            output += f"{console_output.stdout}"
        except Exception as e:
            # logger.error(f"issue id: {issue_id}, issue title: {issue_title}, reason: Invalid syntax., issue prompt: {issue_prompt}")
            
            output += f"{console_output}" if console_output == "" else f"{console_output.stdout}"
    
    return output


def run_ansible(args, config):
    
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
    inventory = config["inventory_file"]
    docker_path = config["docker_dir"]
    private_key = config["private_key"]
    become_password_file = config["become_password_file"]
    
    
    
    def mapper_fn(sample):
        
        if sample["syntax"] == 0:
            ansible_output = None
        else:
            if task == 'module':
                ansible_output = subprocess_ansible_module(
                    sample_data= sample, 
                    yaml_base_path= base_path, 
                    inventory_path= inventory, 
                    docker_path= docker_path, 
                    private_key= private_key, 
                    become_password_file= become_password_file
                )
            elif task == 'github_issue':
                
                ansible_output = subprocess_ansible(
                    sample_data= sample, 
                    yaml_base_path= base_path, 
                    inventory_path= inventory, 
                    docker_path= docker_path, 
                    private_key= private_key, 
                    become_password_file= become_password_file,
                    num_digits=num_digits
                )
        
        sample.update({
            'output' : ansible_output
        })
        
        return sample
    
    output_ds = ds.map(mapper_fn)
    
    trgt_path = file_path
    display.green(f'\nsaving data to {trgt_path} ...')
    output_ds.to_csv(trgt_path)
    


def get_module_based_stat(args, ds, heuristic_list):
    breakpoint()
    if args.type == "syntax":
        stats = {}
        level_list = heuristic_list
        for i in level_list:
            level = i
            
            correct = len(
                ds.filter(
                    lambda example: 
                        example['level'] == level and
                        example['syntax']  == 1 and 
                        example['response'] != "TIMEOUT ERROR"
                    )
                ) 
            total = len(
                ds.filter(
                    lambda example: 
                        example['level'] == level and
                        example['response'] != "TIMEOUT ERROR" 
                    )
                )
            
            stats[i] = {}
            stats[i]['heuristic'] = level
            stats[i]['valid'] = correct
            stats[i]['total'] = total
            stats[i]['second_request'] = sum(
                ds.filter(
                    lambda example: 
                        example['level'] == level and
                        example['response'] != "TIMEOUT ERROR"
                )['second_query']
            )
            
            stats[i]['valid_syntax_first_try'] = len(
                ds.filter(
                    lambda example:  
                        example['level'] == level and
                        example['syntax']  == 1 and 
                        example['second_query'] == 0 and
                        example['response'] != "TIMEOUT ERROR"
                    )
                )
            
            stats[i]['percent'] = (correct / total) * 100 
        
        
        correct = len(
                ds.filter(
                    lambda example: 
                        example['syntax']  == 1 and 
                        example['response'] != "TIMEOUT ERROR"
                    )
                ) 
        total = len(
                ds.filter(
                    lambda example: 
                        example['response'] != "TIMEOUT ERROR" 
                    )
                )
        
        stats['Full'] = {}
        stats['Full']['valid'] = correct
        stats['Full']['total'] = total
        stats['Full']['second_request'] = sum(
                ds.filter(
                    lambda example: 
                        example['response'] != "TIMEOUT ERROR"
                )['second_query']
            )
        stats['Full']['valid_syntax_first_try'] = len(
                ds.filter(
                    lambda example:  
                        example['syntax']  == 1 and 
                        example['second_query'] == 0 and
                        example['response'] != "TIMEOUT ERROR"
                    )
                )
            
        stats['Full']['percent'] = (correct / total) * 100 
        
        display.print_dict(stats)
    
def get_issue_based_stat(args, ds, level_list):
    if args.type == "syntax":
        stats = {}
        for i in level_list:
            level = i
            correct = len(
                ds.filter(
                    lambda example: 
                        example['level'] == level and 
                        example['syntax']  == 1 and 
                        example['response'] != "TIMEOUT ERROR"
                    )
                ) 
            total = len(
                ds.filter(
                    lambda example: 
                        example['level'] == level and
                        example['response'] != "TIMEOUT ERROR"
                    )
                )
            
            stats[i] = {}
            stats[i]['level'] = level
            stats[i]['valid'] = correct
            stats[i]['total'] = total
            
            stats[i]['second_request'] = sum(
                ds.filter(
                    lambda example: example['level'] == level
                )['second_query']
            )
            stats[i]['valid_syntax_first_try'] = len(
                ds.filter(
                    lambda example: 
                        example['level'] == level and 
                        example['syntax']  == 1 and 
                        example['second_query'] == 0 and
                        example['response'] != "TIMEOUT ERROR"
                    )
                )
            
            stats[i]['percent'] = (correct / total) * 100 
        
        display.print_dict(stats)

def generate_statistics(args, config):
    
    base_path = get_base_path(args, config)

    file_path = f"{base_path}/manifest_ds.csv"
    datasets.disable_caching()
    ds = Dataset.from_csv(file_path)
    level_list = [int(x) for x in config["levels"].split(",")]
    heuristic_list = [int(x) for x in config["heuristics"].split(",")]
    
    
    if args.task == 'module':
        display.green(f"\nSyntax Statistics of file: {file_path}\n")
        get_module_based_stat(args, ds, heuristic_list)
    elif args.task == 'github_issue':
        display.green(f"\nSyntax Statistics of file: {file_path}\n")
        get_issue_based_stat(args, ds, level_list)
        