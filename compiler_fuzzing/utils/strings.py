# external imports
import re
from typing import Dict, List, Tuple
from colorama import Fore, Style

"""
this file contains functions for generating strings
"""
def now() -> str:
	"""
	returns a string formatted as YYYYMMDD-HHmmSS (Year, Month, Day, Hour, Minute, Second in order)
	"""

	from datetime import datetime
	return datetime.now().strftime('%Y%m%d-%H%M%S')

def clean_multiline(text: str) -> str:
	"""
	removes unwanted tabs and returns from a multiline string
	"""
	text = re.sub('\n *', '\n', text)
	text = re.sub('\n\t*', '\n', text)
	return text.strip('\n')

def replace_slot(text: str, entries: str) -> str:
    for key, value in entries.items():
        if not isinstance(value, str):
            value = str(value)
        text = text.replace("{{" + key +"}}", value.replace('"', "'").replace('\n', ""))
    return text

def remove_tilde(text: str) -> str:
    return text.split('```')[1] 

def white_space_trail(msg: str) -> List[str]:
    """
    split but keep trailing whitespace at the end of each word

    :param msg:
    :type str:

    :return: list of split tokens
    :rtype: str
    """
    return  re.findall(r'\S+\s*', msg)


#################################################################
### this section contains repetitive colored string functions ###
#################################################################
def green(msg: str):
    """
    returns a given string in green text
    """
    return Fore.GREEN + msg + Style.RESET_ALL

def red(msg: str):
    """
    returns a given string in red text
    """
    return Fore.RED + msg + Style.RESET_ALL

def yellow(msg: str):
    """
    returns a given string in yellow text
    """
    return Fore.YELLOW + msg + Style.RESET_ALL

def blue(msg: str):
    """
    returns a given string in blue text
    """
    return Fore.BLUE + msg + Style.RESET_ALL

def cyan(msg: str):
    """
    returns a given string in cyan text
    """
    return Fore.CYAN + msg + Style.RESET_ALL

def magenta(msg: str):
    """
    returns a given string in magenta text
    """
    return Fore.MAGENTA + msg + Style.RESET_ALL
