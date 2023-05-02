import argparse
from compiler_fuzzing.utils import files, strings

def parse():
    """
    parse the command line arguments
    """

    # define arguments and parse
    parser = argparse.ArgumentParser() 
    parser.add_argument(
        "--config",
        type=str,
        default="{{project_root}}/confs/config.yaml"
    )

    args = parser.parse_args()

    # perform substitutions
    args.config = strings.replace_slot(
        args.config, 
        { 'project_root' : files.get_project_root() }
    )

    return args
