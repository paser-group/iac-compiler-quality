# Level Configurations

Each of these files requires two main variables, `prompt` and `sys_role`.

## prompt
The `prompt` dictionary holds the set of unformatted message strings. 
* `current` is for the strings we are currently using
* `unused` holds previously tested prompts that are not used anymore


## sys_role
The `sys_role` list holds the different types of system role messages.
* `current` is for the strings we are currently using
* `unused` holds previously tested system roles that are not used anymore

## Keywords
areas where we want to insert special data use `{{<keyword>}}` as a placeholder to make it easier to format later
below is a table of keywords that are in use.

| Keyword | Description |
| ------- | ----------- |
| title | the title of the corresponding github issue |

### Example for lv1.yaml
```yaml
prompt :
    - current : 
        - Create a YAML Ansible playbook to exhibit the following issue {{title}}
    - unused :
        - N/A
    
sys_role :
    - current : 
        - You are an AI agent whose purpose is to generate Ansible Playbooks based on github issue titles
    - unused :
        - N/A

```
