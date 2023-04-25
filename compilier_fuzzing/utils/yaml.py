import yaml
from ansible.playbook import Playbook
# from ansible.playbook.playbook import Playbook
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
import yaml
from ..utils.log_utils import record_case


def check_ansible_syntax(playbook_code):
    # Load the YAML code as a dictionary
    playbook_dict = yaml.safe_load(playbook_code)
    # TODO: implement loggerusing these informations: issue_id, issue_prompt, issue_title, logger
    # Load the inventory data
    loader = DataLoader()
    inventory = InventoryManager(loader=loader)

    # Load variables for the playbook
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # Create a new playbook object
    playbook = Playbook.load(playbook_dict, variable_manager=variable_manager, loader=loader)

    try:
        # Check the syntax of the playbook
        playbook.check()
        print("The syntax of the Ansible playbook is valid.")
        return 1
    except Exception as e:
        record_case(f"reason: Invalid syntax., response: {playbook_code}")
        # logger.error(f"issue id: {issue_id}, issue title: {issue_title}, reason: Invalid syntax., issue prompt: {issue_prompt}")
        # record_case(success=False, **{"issue id": issue_id, "issue title": issue_title, "reason": f"Invalid syntax.", "issue prompt": issue_prompt})
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