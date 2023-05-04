from compiler_fuzzing.chat_gpt import create_ansible, validate_ansible
from compiler_fuzzing import arguments, utils, cfg_reader

def main():
    args = arguments.parse()

    if args.procedure == 'generate':
        # read in config data
        cfg = cfg_reader.primary.load(args.config)

        # run the generator
        create_ansible(args, cfg)
    elif args.procedure == 'validate':
        # read in config data
        cfg = cfg_reader.primary.load(args.config)
        
        # run validator
        validate_ansible(args, cfg)
    else:
        raise NotImplementedError(utils.strings.clean_multiline(
            """
            Procedure added to args but case not added to main function in <project root>/lm_toolkit/__init__.py.
            """
        ))
            
