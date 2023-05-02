"""
this file handles the loading of the primary config file
"""
# external imports
import yaml
from typing import Dict, List, Tuple

# local imports
from compiler_fuzzing.utils import files, strings

def load(path_str: str):
    """
    loads the level configs and replaces the keywords

    :param path_str: the path of the file to read
    :type path_str: str

    :rtype: YAML file as a Dict or List
    """


    with open(path_str, 'r') as f:
        cfg = f.read()
    
    cfg = strings.replace_slot(cfg, keywords)
    cfg = yaml.safe_load(cfg)

    return cfg
