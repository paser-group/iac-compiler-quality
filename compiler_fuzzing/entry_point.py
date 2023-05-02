from compiler_fuzzing.chat_gpt import create_ansible
from compiler_fuzzing import arguments, utils, cfg_reader

def main():
    args = arguments.parse()

    if args.procedure == 'generate':
        # read in config data
        cfg = cfg_reader.primary.load(args.config)

        # run the generator
        create_ansible(args, cfg)
    # TODO add procedure for validation
    elif args.procedure == 'validate':
        pass
    else:
        raise NotImplementedError(utils.strings.clean_multiline(
            """
            Procedure added to args but case not added to main function in <project root>/lm_toolkit/__init__.py.
            """
        ))
            
