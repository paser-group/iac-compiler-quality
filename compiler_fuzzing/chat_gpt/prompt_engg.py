from datasets import Dataset
from compiler_fuzzing.utils.strings import replace_slot
from compiler_fuzzing.utils.files import load_yaml

class PromptEngg:
    def __init__(self, config, level, dataset, path_key='taxonomy_filepath', prompt_method='taxonomy'):
        self.config = config
        self.level = level

        file_path = self.config[path_key]
        file_name = f"lv{self.level}.yaml"
        self.prompt_config = load_yaml(f"{file_path}/{file_name}")
        self.system_msg = self.prompt_config['sys_role']['current']
        if prompt_method == 'taxonomy':
            self.dataset = dataset.map(self.update_columns)
        elif prompt_method == 'module':
            self.dataset = dataset.map(self.update_columns_module)
        
        
    def update_columns(self, ds):
        ds["level"] = self.level
        ds["sys_role"] = self.system_msg
        if 'title' in ds.columns:
            title = ds["title"]
        ds["prompt"] = replace_slot(
            self.prompt_config['prompt']['current'], 
            {
                "title" : title,
            }
        )
        
        return ds
    
    def update_columns_module(self, ds):
        ds["level"] = self.level
        ds["sys_role"] = self.system_msg
        
        ds["prompt"] = replace_slot(
            self.prompt_config['prompt']['current'], 
            {
                "module" : ds['name'],
                "attributes": ds['arg_str']
            }
        )
        
        return ds
    
    def get_updated_dataset(self):
        return self.dataset
