from datasets import Dataset
from compiler_fuzzing.utils.strings import replace_slot
from compiler_fuzzing.utils.yaml import get_config

class PromptEngg:
    def __init__(self, config, level, dataset):
        self.config = config
        self.level = level
        self.dataset = dataset.map(self.update_columns)
        
        
    def update_columns(self, ds):
        ds["level"] = self.level
        file_path = self.config['taxonomy_filepath']
        file_name = f"lv{self.level}.yaml"
        prompt_config = get_config(name=f"{file_path}/{file_name}")
        breakpoint()
        ds["sys_role"] = prompt_config["sys_role"]["current"]
        title = ds["TITLE"]
        ds["prompt"] = replace_slot(prompt_config["sys_role"]["current"], {
            "title": title
            })
        
        return ds
    
    def get_updated_dataset(self):
        return self.dataset
