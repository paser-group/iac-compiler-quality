import argparse

def parse():

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="confs/config.yaml")
    args = parser.parse_args()

    return args
