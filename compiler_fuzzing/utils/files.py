"""
this file contains functions regarding file handling. and directories
"""
# external imports
from pathlib import Path
import os
import yaml
import pickle
from typing import Dict, List, Tuple

# local imports
from compiler_fuzzing.utils import validate

def get_project_root() -> str:
    """
    use this to get the root directory of the project

    :rtype str: the root directory of the project
    """
    return str(Path(__file__).parent.parent.parent)

def get_full_path(path_str, check_exist=False) -> str:
    """
    converts the input into an absolute path if recognized as a relative path

    :param path_str: the path of the given file

    :param validate: if True validates if the path exists

    :rtype str: the full path of the input
    """

    # convert to absolute path
    path = os.path.abspath(path_str)

    # check if path exists. raise error otherwise
    if check_exist : validate.path_exists(path)

    return path

def dirname(path_str: str) -> str:
    """
    clips the last bit of the path string

    :param path_str: the directory string
    :type path_str: str

    :rtype str: the directory of the input
    """

    return os.path.dirname(path_str)

def get_fname(path_str: str) -> str:
    """
    extracts the file name from a given path string

    :param path_str: the path string
    :type path_str: str

    :rtype str: the desired file name
    """
    
    return os.path.basename(path_str)

def split_dir_fname(path_str: str) -> Tuple[str, str]:
    return (
        dirname(path_str),
        get_fname(path_str)
    )


def homedir() -> str:
    """
    returns the home directory

    :rtype str: the home directory
    """
    return str(Path.home())

def create_path(path_str):
	if not valid_path(path_str):
		os.mkdir(path_str)

def count_lines(path: str) -> int:
    """
    counts the number of lines in a file

    :param path: the full path of the file

    :rtype int: the number of lines in the file

    :raises: FileNotFound
    """

    # check if path exists. raise error otherwise
    validate.path_exists(path)

    # count the number of lines in the file
    with open(path, 'r') as f:
        return len(f.readlines())

def save_pkl(src_obj: object, path_str: str):
    """
    pickles an object and saves it to the given directory
    """

    with open(path_str, 'wb') as f:
        pickle.dump(src_obj, f)

def load_pkl(path_str: str) -> object:
    """
    loads a pickled object 
    """

    with open(path_str, 'rb') as f:
        src_obj = pickle.load(f)
    
    return src_obj

def valid_path(path_str: str) -> bool:
    """
    checks if a given path string exists

    :param path_str: input path
    :type path_str: str

    :rtype bool: True if path exists else false
    """
    return os.path.exists(path_str)

def load_yaml(path_str: str):
    """
    loads a yaml file

    :param path_str: 
    :type path: str
    """

    # check if path exists. raise error otherwise
    validate.path_exists(path_str)

    # read config
    with open(path_str, 'r') as f:
        cfg = yaml.safe_load(f)
    return cfg
