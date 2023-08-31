import argparse
import argcomplete
from compiler_fuzzing.utils import files, strings

def parse():
    """
    parse the command line arguments
    """

    ######################### begin arg definitions ######################### 

    # define arguments and parse
    parser = argparse.ArgumentParser() 

    # create subparser for procedures
    subparser = parser.add_subparsers(
        description='decides on which procedure to run',
        required=True,
        dest='procedure',
    )

    # add subparser for playbook generation
    parser_gen = subparser.add_parser(
        'generate',
        description='generates ansible playbooks'
    )
    parser_gen.add_argument(
        '-c',
        '--config',
        help='config path',
        type=str,
        default="{{PROJECT_ROOT}}/confs/config.yaml",
    )

    parser_gen.add_argument(
        '--debug',
        help='used for testing the create_ansible function',
        action='store_true',
        default=False,
    )

    parser_gen.add_argument(
        '--limit',
        help='used to limit the amount of samples generated',
        type=int,
        default=-1,
    )
    
    parser_gen.add_argument(
        '--prompt_method',
        help='used to determine the nature of prompt. options: [taxonomy, taxonomy-heu]',
        type=str,
        default="taxonomy",
    )

    # subparser for validation
    parser_gen = subparser.add_parser('validate')
    parser_gen.add_argument(
        '-c',
        '--config',
        help='config path',
        type=str,
        default="{{PROJECT_ROOT}}/confs/config.yaml",
    )

    parser_gen.add_argument(
        '--debug',
        help='used for testing the create_ansible function',
        action='store_true',
        default=False,
    )

    parser_gen.add_argument(
        '--timestamp',
        help='used to read from a specific timestamp generated data. (Default: most recent)',
        type=str,
        default=None,
    )
    
    parser_gen.add_argument(
        '--task',
        help='Used to define which task we are validating on. options: [module, github_issue]',
        type=str,
        default='github_issue',
    )
    
    # subparser for getting output
    parser_gen = subparser.add_parser('run')
    parser_gen.add_argument(
        '-c',
        '--config',
        help='config path',
        type=str,
        default="{{PROJECT_ROOT}}/confs/config.yaml",
    )

    parser_gen.add_argument(
        '--debug',
        help='used for testing the create_ansible function',
        action='store_true',
        default=False,
    )

    parser_gen.add_argument(
        '--timestamp',
        help='used to read from a specific timestamp generated data. (Default: most recent)',
        type=str,
        default=None,
    )
    
    parser_gen.add_argument(
        '--task',
        help='Used to define which task we are validating on. options: [module, github_issue]',
        type=str,
        default='github_issue',
    )
    
    # Subperser for statistics
    parser_gen = subparser.add_parser('stat')
    parser_gen.add_argument(
        '-c',
        '--config',
        help='config path',
        type=str,
        default="{{PROJECT_ROOT}}/confs/config.yaml",
    )

    parser_gen.add_argument(
        '--debug',
        help='used for testing the create_ansible function',
        action='store_true',
        default=False,
    )

    parser_gen.add_argument(
        '--timestamp',
        help='used to read from a specific timestamp generated data. (Default: most recent)',
        type=str,
        default=None,
    )
    
    parser_gen.add_argument(
        '--type',
        help='used to generate type of statistics. (Default: syntax)',
        type=str,
        default="syntax",
    )
    
    parser_gen.add_argument(
        '--task',
        help='Used to define which task we are validating on. options: [module, github_issue]',
        type=str,
        default='github_issue',
    )

    # subparser for unit testing
    parser_gen = subparser.add_parser('unit_test')
    parser_gen.add_argument(
        '-c',
        '--config',
        help='config path',
        type=str,
        default="{{PROJECT_ROOT}}/confs/config.yaml",
    )

    # subparser for generating module list
    parser_gen = subparser.add_parser('gen_module_list')
    parser_gen.add_argument(
        '-c',
        '--config',
        help='config path',
        type=str,
        default="{{PROJECT_ROOT}}/confs/config.yaml",
    )
    # subparser for generating module list
    parser_gen = subparser.add_parser('gen_module_ansible')
    parser_gen.add_argument(
        '-c',
        '--config',
        help='config path',
        type=str,
        default="{{PROJECT_ROOT}}/confs/config.yaml",
    )

    parser_gen.add_argument(
        '--debug',
        help='used for testing the create_ansible function',
        action='store_true',
        default=False,
    )
    
    parser_gen.add_argument(
        '--limit',
        help='used to limit the amount of samples generated',
        type=int,
        default=-1,
    )
    
    ######################### end arg definitions ######################### 

    # parse
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    # perform substitutions
    args.config = strings.replace_slot(
        args.config, 
        { 'PROJECT_ROOT' : files.get_project_root() }
    )

    return args
