"""
this file contains functions for printing things in a certain format
"""
# external imports
from colorama import Fore, Style
import os

def title(title_str: str, fill_char: str='='):
	"""
	prints the given title centered in the terminal and surrounded by fill_char 

	:param title_str: the text to print in the middle
	:type title_str: str

	:param fill_char: the character to be used to fill out the rest of the line. (default '='
	:type fill_char: str
	"""

	# get terminal size
	col, lines = os.get_terminal_size()

	# print the title
	print('\n' + title_str.center(col, fill_char) + '\n')

def binary_prompt(message: str) -> bool:
	"""
	used to prompt the user for any yes or no options

	:param message: the message to be displayed before prompting

	:rtype bool: yes or no converted to true or false
	"""

	choice = input(f'{message} (y/n): ').lower()
	if choice == 'y' or choice == 'yes':
		return True
	else:
		return False

def green(msg: str, end='\n'):
    """
    prints a string in green text
    """
    print(Fore.GREEN + msg + Style.RESET_ALL)

def red(msg: str, end='\n'):
    """
    prints a string in red text
    """
    print(Fore.RED + msg + Style.RESET_ALL)
