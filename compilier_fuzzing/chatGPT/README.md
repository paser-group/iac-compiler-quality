# ChatGPT GitHub Issue YAML Playbook Generation
This Python script generates YAML Ansible playbooks to help test and exhibit issues found in GitHub repositories.

The script uses OpenAI's ChatGPT API to generate syntactically correct Ansible YAML Playbooks based on GitHub issues stored in a Pandas dataframe for evaluation. The generated playbooks are saved in the same dataframe and also exported to a Feather file.

## Prerequisites
- **`openai`**  module
- **`pandas`**  module
- **`yaml`**  module
- OpenAI API key with Chat and File Access scopes
- Feather file with GitHub issues saved in a Pandas dataframe



## Usage
1.Open the Python script in a text editor or integrated development environment (IDE).
- Update the **`openai.organization`** variable with your OpenAI organization ID.
- Replace the **`openai.api_key`** variable with your OpenAI API key.
- Update the path of the Feather file containing GitHub issues stored in a Pandas dataframe.
- Update the file path of the output Feather file where you want to save the updated Pandas dataframe with generated YAML playbooks.
- Adjust the **`generation_limit`** variable to limit the number of YAML playbooks generated. 

2. Run the script using python chatgpt_generate_playbooks.py.
The script will generate YAML Ansible playbooks for each issue in the input Feather file using OpenAI's ChatGPT API. The generated playbooks will be saved in the same dataframe and also exported to a Feather file.
3. Check the Valid column in the output Feather file to verify that the generated YAML playbooks are syntactically correct. Invalid YAML syntax will be marked with a 0 in the Valid column. You can also manually verify the generated playbooks by opening the output Feather file and checking the Output column.
4. Use the generated YAML Ansible playbooks to test and exhibit issues found in GitHub repositories.

**Note**: If you encounter issues with OpenAI's ChatGPT API, refer to the OpenAI documentation for more information and troubleshooting steps as the API regularly is updated and changes may cause inconsitiencies or the scripts to fail.
