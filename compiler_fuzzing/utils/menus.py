# external imports
from simple_term_menu import TerminalMenu
import os
import sys
from pathlib import Path

# local imports
from . import files

def file_explorer(prompt, start_path=None):
    """this displays a menu for finding and returning a desired file path

    :rtype str:
    """
    cwd = os.getcwd() if start_path is None else files.full_path(start_path)
    directory = ['../'] + sorted(os.listdir(cwd))
    
    while True:
        menu = TerminalMenu(
            directory,
            title=f'\n{prompt}: {cwd}',
            skip_empty_entries=True,
            clear_screen=True,
            show_shortcut_hints=True,
            show_shortcut_hints_in_status_bar=False,
        )

        # loop until exit or choice has been made
        while True:
            choice = menu.show()

            # exits if the user quit the menu
            if choice is None:
                if binary_prompt('exit?'):
                    sys.exit()
            else:
                break

        fname = directory[choice]
        if fname == '../':
            target = str(Path(cwd).parent)
        else:
            target = f'{cwd}/{fname}'


        # check if the file is good
        if os.path.isfile(target):
            choice = binary_prompt(f'is {target} correct?')
            if choice:
                return target
        else:
            cwd = target
            directory = ['../'] + sorted(os.listdir(cwd))


def yes_no(message: str, default_no: bool=True) -> bool:
    """
    used to prompt the user for any yes or no options

    Input
        message[str]: the message to be displayed before prompting
        default_no[bool]: sets the default action. if default_no then prompt returns true unles 'n' or  'no' is specified

    Return
        bool: yes or no converted to true or false
    """

    choice = input(f'{message} (y/n): ').lower()
    if default_no:
        return not choice in ['n', 'no']
    else:
        return choice in ['y', 'yes']
