"""
this file contains functions for printing things in a certain format
"""

def print_title(title_str, fill_char='='):
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

def prompt_yes_no(message):
	"""
	used to prompt the user for any yes or no options

	:param message: the message to be displayed before prompting

	:rtype int:
	"""

	choice = input(f'{message} (y/n): ').lower()
	if choice == 'y' or choice == 'yes':
		return 1
	else:
		return 0
