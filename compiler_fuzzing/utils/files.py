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

    :return: the root directory of the project
    :rtype: str
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

    :return: the directory of the input
    :rtype: str
    """

    return os.path.dirname(path_str)

def get_fname(path_str: str) -> str:
    """
    extracts the file name from a given path string

    :param path_str: the path string
    :type path_str: str
    
    :return:the desired file name
    :rtype: str 
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
    
    :return: the home directory
    :rtype: str
    """
    return str(Path.home())

def create_path(path_str, parents=True, exist_ok=True):
    if not valid_path(path_str):
        Path(path_str).mkdir(
            parents=parents,
            exist_ok=exist_ok
        )


def count_lines(path: str) -> int:
    """
    counts the number of lines in a file

    :param path: the full path of the file

    :return: the number of lines in the file
    :rtype: int

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

    :return: True if path exists else false
    :rtype: bool
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

def count_files_in(path_str: str, match_str: str=None) -> int:
    """
    counts the number of files in a given path. if given a file, its containing directory is used.
    if match_str is provided, this function only counts files that contain it as a substring

    :param path_str: input path
    :type path_str: str

    :param match_str: the substring that we want to match with files
    :type match_str: str

    :return: number of files in the directory
    :rtype: int

    :raises: FileNotFound
    """

    validate.path_exists(path_str)

    files = os.listdir(path_str)
    files = [f for f in files if match_str in f]

    return len(files)

def list(path_str: str) -> List:
    
    validate.path_exists(path_str)

    return os.listdir(path_str)

def write_file(path_str: str, content: str):
    """
    saves a  yaml file

    :param path_str: 
    :type path: str

    :param content: the data to be written to file
    :type content: str

    :raises: FileNotFoundError
    """

    validate.path_exists(dirname(path_str))
    with open(path_str, 'w') as f:
        f.write(content)
