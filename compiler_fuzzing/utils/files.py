"""
this file contains functions regarding file handling. and directories
"""
# external imports
from pathlib import Path
import os
import yaml
import pickle

# local imports
from compiler_fuzzing.utils import validate

def get_project_root():
	"""
	use this to get the root directory of the project
	"""
	return str(Path(__file__).parent.parent.parent)

def count_lines(path):
	"""
	counts the number of lines in a file

	:param path: the full path of the file
	:raises: FileNotFound
	"""

	# check if path exists. raise error otherwise
	validate.path_exists(path)

	# count the number of lines in the file
	with open(path, 'r') as f:
		return len(f.readlines())

def parent_dir(path_str):
	"""
	clips the last bit of the path string

	:param path_str: the directory string
	:type path_str: str
	"""

	return str(Path(path_str).parent)

def save_pkl(src_obj, path_str):
	"""
	pickles an object and saves it to the given directory
	"""

	with open(path_str, 'wb') as f:
		pickle.dump(src_obj, f)

def load_pkl(path_str):
	"""
	loads a pickled object 
	"""

	with open(path_str, 'rb') as f:
		src_obj = pickle.load(f)
	
	return src_obj

def valid_path(path_str):
	"""
	checks if a given path string exists
	"""
	return os.path.exists(path_str)

def load_yaml(path_str):
	"""
	loads a yaml file
	"""

	# check if path exists. raise error otherwise
	validate.path_exists(path_str)

	# read config
	with open(path_str, 'r') as f:
		cfg = yaml.safe_load(f)
	return cfg
