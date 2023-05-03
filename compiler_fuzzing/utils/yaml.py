import subprocess
import yaml
from compiler_fuzzing.utils.logs import record_case
from compiler_fuzzing.utils.files import valid_path
from compiler_fuzzing.utils import display 


def check_ansible_syntax(sample_data, yaml_base_path):
    level = sample_data["level"]
    issue_id = sample_data["ID"]
    playbook_path = f"{yaml_base_path}/lv{level}/{issue_id}.yaml"
    if not valid_path(playbook_path):
        return 0

    try:
        # Check the syntax of the playbook
        subprocess.check_output(['ansible-playbook', playbook_path, '--syntax-check'], stderr=subprocess.STDOUT)
        
        display.green("Ansible syntax check passed for playbook: ", playbook_path)
        return 1
    except Exception as e:
        # logger.error(f"issue id: {issue_id}, issue title: {issue_title}, reason: Invalid syntax., issue prompt: {issue_prompt}")
        record_case(success=False, **{"issue id": sample_data["ID"], "issue title": sample_data["TITLE"], "reason": f"{e}", "issue prompt": sample_data["prompt"]})
        return 0



def get_config(name='config.yaml'):
    config = yaml.load(open(name, "r"), Loader=yaml.FullLoader)
    return config

def get_yaml_data(text):
    # TODO: implement loggerusing these informations: issue_id, issue_prompt, issue_title, logger
    try:
        data = text.split("```")[1]
        code = yaml.safe_load(data)
        #print("Valid YAML syntax")
        return 1
    except:
        #print("Invalid YAML syntax:", error)
        code = ''
        record_case(f"reason: Invalid syntax., response: {text}")
        # record_case(success=False, **{"issue id": issue_id, "issue title": issue_title, "reason": f"Invalid syntax.", "issue prompt": issue_prompt})
        return 0
