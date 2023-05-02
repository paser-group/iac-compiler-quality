from compiler_fuzzing.chat_gpt import create_ansible
from compiler_fuzzing import arguments, utils

def main():
    args = arguments.parse()

    if args.procedure == 'generate':
        create_ansible(args)
    else:
        raise NotImplementedError(utils.strings.clean_multiline(
            """
            Procedure added to args but case not added to main function in <project root>/lm_toolkit/__init__.py.
            """
        ))
            
    breakpoint()
