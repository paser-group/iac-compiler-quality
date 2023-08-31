from datasets import Dataset
from compiler_fuzzing.utils.strings import replace_slot
from compiler_fuzzing.utils.files import load_yaml

class PromptEngg:
    def __init__(self, config, level, dataset, path_key='taxonomy_filepath', prompt_method='taxonomy', module_file='heu'):
        self.config = config
        self.level = level

        if prompt_method == 'taxonomy':
            file_path = self.config[path_key]
            file_name = f"lv{self.level}.yaml"
            self.prompt_config = load_yaml(f"{file_path}/{file_name}")
            self.system_msg = self.prompt_config['sys_role']['current']
            self.dataset = dataset.map(self.update_columns)
        elif prompt_method == 'module':
            file_path = self.config[path_key]
            file_name = f"lv{module_file}.yaml"
            self.prompt_config = load_yaml(f"{file_path}/{file_name}")
            self.system_msg = self.prompt_config['sys_role']['current']
            self.dataset = dataset.map(self.update_columns_module)
        elif prompt_method == 'taxonomy-heu':
            file_path = self.config[path_key]
            file_name = f"lv{self.level}.yaml"
            self.prompt_config = load_yaml(f"{file_path}/{file_name}")
            self.system_msg = self.prompt_config['sys_role']['current']
            self.dataset = dataset.map(self.update_columns_heu)
        
        
    def update_columns(self, ds):
        ds["level"] = self.level
        ds["sys_role"] = self.system_msg
        #if 'title' in ds.columns:
        try:
            if 'title' in ds.columns:
                title = ds["title"]
        except:
            if 'title' in dict(ds).keys():
                title = ds["title"]
        ds["prompt"] = replace_slot(
            self.prompt_config['prompt']['current'], 
            {
                "title" : title,
            }
        )
        
        return ds
    
    def update_columns_heu(self, ds):
        ds["level"] = self.level
        ds["sys_role"] = self.system_msg
        # breakpoint()
        heuristic = self.config[f'{str(ds["MAIN-CATEG"]).lower()}_heuristics']
        heuristic_text = ""
        if heuristic:
            heuristic_text = f"Your playbook should also incorporate test cases based on the following heuristic: {heuristic}"
        try:
            if 'title' in ds.columns:
                title = ds["title"]
        except:
            if 'title' in dict(ds).keys():
                title = ds["title"]
        ds["prompt"] = replace_slot(
            self.prompt_config['prompt']['current'], 
            {
                "title" : title,
                "body" : ds["body"],
                "category" : ds["MAIN-CATEG"],
                "heuristic" : heuristic_text
            }
        )
        
        return ds
    
    def update_columns_module(self, ds):
        ds["level"] = f"{self.level}"
        ds["sys_role"] = self.system_msg
        
        ds["prompt"] = replace_slot(
            self.prompt_config['prompt']['current'], 
            {
                "module" : ds['name'],
                "attributes": ds['arg_str'],
                "desc_short": ds['desc_short'],
                "heuristic": self.config["type_heuristics"][f"h{self.level}"]
            }
        )
        
        return ds
    
    def get_updated_dataset(self):
        return self.dataset
