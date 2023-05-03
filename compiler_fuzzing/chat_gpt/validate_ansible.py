from datasets import Dataset
import datasets

# internal imports
from compiler_fuzzing.utils import (
    yaml,
    display,
)

def validate_ansible(args, config):
    
    base_path = f"{config['output_dir']}/{args.timestamp}"
    file_path = f"{base_path}/manifest_ds.csv"
    datasets.disable_caching()
    ds = Dataset.from_csv(file_path)
    
    def mapper_fn(sample):
        sample.update({
            'syntax' : yaml.check_ansible_syntax(sample, base_path)
        })
        return sample
    
    output_ds = ds.map(mapper_fn)
    
    trgt_path = file_path
    display.green(f'\nsaving data to {trgt_path} ...')
    output_ds.to_csv(trgt_path)
    