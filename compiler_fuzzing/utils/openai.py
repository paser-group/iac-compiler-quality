
import openai


def get_response(prompt, config):
    openai.api_key = config["openai"]["key"]
    openai.organization = config["openai"]["organization"]
    
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant who will generate syntactically correct Ansible YAML Playbook for testing purposes. Do not include any explanation or context or introduction statement. Make sure to include ``` before and after Ansible code to denote the YAML section"},
                {"role": "user", "content": prompt}
            ]
        )

    return resp