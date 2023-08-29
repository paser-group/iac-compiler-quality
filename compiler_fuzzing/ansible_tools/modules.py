"""
this module contains the code for creating the dataset of ansible modules that we will test
"""
# external imports
import re
import datasets
import subprocess
import sys
from tqdm import tqdm
from datasets import Dataset
import os

# local imports
from compiler_fuzzing.chat_gpt import (
    check_syntax_string,
    PromptEngg
)
from compiler_fuzzing.utils import (
    ChatSession,
    strings,
    display,
    menus,
    files,
)

def generate_playbooks(output_ds, config, base_output_path, heuristic_list=['base']):
    display.green(f'\ngenerating YAML files to {base_output_path}...')

    # get directories for each level
    # output_lv_path = f'{base_output_path}/base'
    output_lv_paths = [
        f'{base_output_path}/lv{lv}'
        for lv in heuristic_list
    ]
    
    # files.create_path(output_lv_path)
    for pth in output_lv_paths : files.create_path(pth)

    # breakpoint()
    # write files to output directory
    for i, sample in enumerate(tqdm(output_ds, desc='generating playbooks', total=len(output_ds))):
        if sample['code'] != '':
            codes = sample['code'].split(";;;;")
            for j, code in enumerate(codes):
                
                # module_path = f'{output_lv_path}/{sample["name"]}'
                module_path = output_lv_paths[
                    heuristic_list.index(int(sample['level']))
                    ]+ \
                    f'/{sample["name"]}'
                files.create_path(module_path)
                file_path = f"{module_path}/{j}.yaml"
                files.write_file(file_path, code)

def generate_ansible_for_modules(args, config):
    
    # args.limit = 3
    # level_list = [int(x) for x in config["module_prompt_levels"].split(",")]
    # args.limit = args.limit * len(level_list)
    ds = Dataset.from_csv(config['module_data_dir'])
    
    heuristic_list = [int(x) for x in config["heuristics"].split(",")]
    args.limit = args.limit * len(heuristic_list)
    
    output_ds = generate_manifest_ds(args, config, ds, heuristic_list)

    # build output path string
    timestamp = strings.now()
    if not args.debug: 
        base_output_path = \
            config['module_output_dir'] + \
            f'/{timestamp}'
    else:
        base_output_path = f'{config["module_output_dir"]}/debug'
    files.create_path(base_output_path)

    trgt_path = base_output_path + '/manifest_ds.csv'
    display.green(f'\nsaving data to {trgt_path} ...')
    output_ds.to_csv(trgt_path)

    # generate output configs
    generate_playbooks(output_ds, config, base_output_path, heuristic_list)

    # display status messages
    num_blanks = output_ds[:]['code'].count('')
    display.green(
        f'\n\nGenerated {len(output_ds) - num_blanks} Ansible Playbook(s) out of {len(output_ds)}\n' + \
            f'{num_blanks} example(s) generated no code', 
        end='\n\n'
    )
    display.title('Finished Playbook Generation')

    # cleanup cache
    ds.cleanup_cache_files()
    if args.debug : breakpoint()
    
def generate_manifest_ds(args, cfg, ds, heuristic_list=['base']):

    key = 'module_taxonomy_filepath'
    ds.cleanup_cache_files()
    generators = [
        PromptEngg(
            config=cfg, 
            level=lvl, 
            dataset=ds, 
            path_key=key, 
            prompt_method='module', 
            module_file='heu'
            ) 
        for lvl in heuristic_list
        ]
    ds = datasets.interleave_datasets(
        [gen.get_updated_dataset() for gen in generators]
    )
    # breakpoint()
    second_query = []
    response = []
    first_response = []
    
    
    for i, sample in enumerate(tqdm(ds, desc='collecting chatgpt responses', total=len(ds))):
        if i == args.limit : break

        session = ChatSession(
            key = cfg['openai']['key'],
            org= cfg["openai"]["organization"],
            model= cfg['model'],
            system_msg=sample['sys_role']
        )
        try:
            reply = session.get_response(sample['prompt'])
            codes = strings.extract_yamls(reply) \
                if '```' in reply \
                else [""]
            
            flag = 0
            for code in codes:
                # breakpoint()
                if re.match(r'^yaml', code) is not None:
                    code = code[4:].strip()
                correct_syntax = check_syntax_string(code, cfg)
                flag = flag or correct_syntax
            second_call = 0
            first_reply = reply
            if not correct_syntax:
                second_call = 1
                reply = session.get_response(cfg["syntax_nudge"])
                
            second_query.append(second_call)
            response.append(reply)
            first_response.append(first_reply)
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            sys.exit(0)
        except Exception as e:
            
            display.red(f'timeout error on sample {i}')
            response.append('TIMEOUT ERROR')
            second_query.append(0)
            first_response.append('TIMEOUT ERROR')

    # truncate dataset to accomodate amount of responses generated
    output_ds = ds.select(range(len(response)))
    assert len(response) == len(second_query)
    assert len(response) == len(first_response)
    
    # append columns to dataset
    output_ds = output_ds.add_column('response', response)
    output_ds = output_ds.add_column('second_query', second_query)
    output_ds = output_ds.add_column('first_response', first_response)

    # extract code from the responses and add to a new column
    def mapper_fn(sample):
        # extract code from response
        # breakpoint()
        codes = strings.extract_yamls(sample['response']) \
                if '```' in sample['response'] \
                else ''
        
        
        if codes != '':
            lst = []
            for code in codes:
                if re.match(r'^yaml', code) is not None:
                    code = code[4:].strip()
                    lst.append(code)
            codes = ';;;;'.join(lst)
                
        sample.update({
            'code' : codes,
        })
        return sample
    
    output_ds = output_ds.map(mapper_fn)
    
    return output_ds

def build_module_list(args, cfg):

    """
    executes and collects data on the outputs of 'ansible-doc -l'. 
    
    Input
        args[argparse.Namespace]: the command line arguments
        cfg[Dict]: the config values
    """

    ########### unpack values from cfg ########### 

    target_collections = cfg['module_collections']
    save_dir = cfg['module_data_dir']

    ##############################################

    # check if file exists
    if files.path_exists(save_dir):
        choice = menus.binary_prompt(
            f'save location ({save_dir}) already exists. overwrite?',
            default=False
        )
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
    for module in tqdm(
        modules,
        total=len(modules),
        desc='aggregating module information'
    ):
        
        # split line into basics
        module = module.split()
        mod_name = module[0]
        desc_short = ' '.join(module[1:])

        # get full desc
        desc_full = subprocess.check_output(['ansible-doc', mod_name]).decode()
        module_args, arg_types = get_module_args(desc_full)
        
        module_arg_list = module_args.split('\n')
        arg_types_list = arg_types.split('\n')
        arg_str = ""
        for i in range(len(module_arg_list)):
            arg_str += f"{module_arg_list[i]} ({arg_types_list[i]}), "


        ds.append({
            'name': mod_name,
            'desc_short': desc_short,
            'desc_full': desc_full,
            'args': module_args,
            'arg_types': arg_types,
            'arg_str': arg_str,
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
            
