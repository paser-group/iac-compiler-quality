"""
this file contains functions for printing things in a certain format
"""
# external imports
from colorama import Fore, Style
import os

# local imports
from . import strings

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
    
def print_dict(dictionary, indent=0):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            green(f"{' ' * indent}{key}:")
            print_dict(value, indent + 2)
        elif isinstance(value, list):
            green(f"{' ' * indent}{key}:")
            for item in value:
                if isinstance(item, dict):
                    print_dict(item, indent + 2)
                else:
                    green(f"{' ' * (indent + 2)}{item}")
        else:
            green(f"{' ' * indent}{key}: {value}")

def print_list(data_list, indent=0):
    if all(isinstance(item, str) for item in data_list):
        green('\n'.join(f"{' ' * indent}{item}" for item in data_list))
    elif all(isinstance(item, dict) for item in data_list):
        for index, dictionary in enumerate(data_list, start=1):
            green(f"{' ' * indent}Dictionary {index}:")
            print_dict(dictionary, indent + 2)
    else:
        red("Invalid data type in the list.")

def red(msg: str, end='\n'):
    """
    prints a string in red text
    """
    print(Fore.RED + msg + Style.RESET_ALL)


######################################################################################
### this section contains repetitive code for printing strings with headers on them ###
######################################################################################

def with_header(msg: str, header, color='green', end='\n'):
    """
    prints a message in the format '[<header>] <msg>' where the color <header> can be changed by the <color> argument

    Input:
        msg: str - the message to be displayed
        header: str - the header message. usually a single word
        color: str - the desired color for the header
    """
    colorizer = {
        'green': strings.green,
        'red': strings.red,
        'yellow': strings.yellow,
        'blue': strings.blue,
        'cyan': strings.cyan,
        'magenta': strings.magenta,
    }

    if color not in colorizer:
        raise ValueError(f'The color \'{color}\' is not supported')

    print('[' + colorizer[color](header) + '] ' + msg, end=end)

def warning(msg: str, end='\n'):
    with_header(msg, 'WARNING', color='yellow', end=end)

def error(msg: str, end='\n'):
    with_header(msg, 'ERROR', color='red', end=end)

def ok(msg: str, end='\n'):
    with_header(msg, 'OK', color='green', end=end)
    
def note(msg: str, end='\n'):
    with_header(msg, 'NOTE', color='magenta', end=end)

def in_progress(msg: str, end='\n'):
    with_header(msg, 'IN PROGRESS', color='blue', end=end)

def testing(msg: str, end='\n'):
    with_header(msg, 'TESTING', color='blue', end=end)

def done(msg: str=None, end='\n'):
    if msg is None:
        with_header('', 'DONE', color='green', end=end)
    else:
        with_header(msg, 'DONE', color='green', end=end)

def test_passed(end='\n'):
    with_header('', 'PASS', color='green', end=end)

def fail(msg: str, end='\n'):
    with_header(msg, 'FAIL', color='red', end=end)

def review(msg: str, end='\n'):
    with_header(msg, 'FOR REVIEW', color='yellow', end=end)

def exception(msg: str, end='\n'):
    with_header(msg, 'EXCEPTION CONTENT', color='red', end=end)
