"""
this file contains functions used for error checking
"""
import os
from colorama import Fore, Style

def path_exists(path, extra_info=None):
	# build message string
	message = f'The path \'{path}\' does not exist.'
	if message:
		message += f'\n{extra_info}'

	if not os.path.exists(path):
		raise FileNotFoundError(Fore.RED + message + Style.RESET_ALL)

def in_dict(key, dictionary, dict_name):
	if key not in dictionary:
		raise KeyError(
			Fore.RED +
			f'the key \'{str(key)}\' was not found in the dictionary named \'{dict_name}\'' +
			Style.RESET_ALL
		)
