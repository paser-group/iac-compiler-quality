"""
this module contains the code for creating the dataset of ansible modules that we will test
"""
# external imports
import re
import subprocess
import sys
from tqdm import tqdm
from datasets import Dataset

# local imports
from compiler_fuzzing.utils import (
    display,
    menus,
    files,
)

def build_module_list(args, cfg):

    ########### unpack values from cfg ########### 

    target_collections = cfg['module_collections']
    save_dir = cfg['module_data_dir']

    ##############################################

    # check if file exists
    if files.path_exists(save_dir):
        choice = menus.binary_prompt(f'save location ({save_dir}) already exists. overwrite?', default=False)
        if choice == False:
            display.done('Exiting without creating new dataset ...')
            sys.exit()

    
    # get module list
    modules = subprocess.check_output(['ansible-doc', '-l']).decode()
    modules = modules.split('\n')

    # filter out samples that aren't in target_collections
    modules = list(filter(
        lambda module: any(name in module for name in target_collections),
        modules
    ))

    # start building dataset by first building list of dictionaries with desired attributes
    ds = []
    for module in tqdm(modules, total=len(modules), desc='aggregating module information'):
        
        # split line into basics
        module = module.split()
        mod_name = module[0]
        desc_short = ' '.join(module[1:])

        # get full desc
        desc_full = subprocess.check_output(['ansible-doc', mod_name]).decode()
        module_args, arg_types = get_module_args(desc_full)

        ds.append({
            'name': mod_name,
            'desc_short': desc_short,
            'desc_full': desc_full,
            'args': module_args,
            'arg_types': arg_types,
        })

    # convert to huggingface dataset and save to cfg['module_data_dir']
    ds = Dataset.from_list(ds)
    ds.to_csv(save_dir)

    display.done(f'module dataset saved to {save_dir}')

# TODO should proably handle sub-arguments at some point
def get_module_args(desc_full):
    """
    extracts the arguments from an ansible module description.
    in other words, module arguments are extracted from the output of "ansible-doc <module name>"
    which is assigned to <desc_full>

    Input:
        desc_full[str]: the description of the module

    Return:
        args[Tuple[list[str], list[str]]]: a tuple of th
    """
    
    desc_split = desc_full.split('\n')

    args = []
    types = []

    # get truncation indices
    try:
        trunc_start = desc_full.index('OPTIONS')
    except Exception as e:
        trunc_start = 0

    try:
        trunc_end = desc_full.index('EXAMPLES')
    except Exception as e:
        trunc_end = len(desc_full)

    # trim the description to keep out unwanted string matches
    desc_trim = desc_full[trunc_start:trunc_end]

    # split the trimmed description into 'blocks' that are separated by 2 newline characters
    desc_trim = desc_trim.split('\n\n')

    for block in desc_trim:
        lines = block.split('\n')
        arg_name = None
        type_list = []
        for line in lines:
            if re.match(r'^[-=]', line):
                # extract argument
                arg_name = line.split()[1]

            elif 'type:' in line and arg_name is not None:
                # append
                type_list.append(line.split()[-1])
        if arg_name is not None:
            # append arg
            args.append(arg_name)

            # append type
            tp = type_list[-1] if len(type_list) > 0 else 'None'
            types.append(tp)

    # convert to strings
    args = '\n'.join(args)
    types = '\n'.join(types)

    return (args, types)
            
