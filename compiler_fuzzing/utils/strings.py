import re

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
