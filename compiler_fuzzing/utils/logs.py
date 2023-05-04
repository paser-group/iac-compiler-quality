import json
import logging
import os
from . import files

def get_log_files(config):
    files.create_path(files.get_project_root() + "/logs")
    handler = logging.StreamHandler()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    log_file = config["log_file"]
    if log_file:
        filehandler = logging.FileHandler(log_file)
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        
    return logger, handler

def record_case(success, **args):
    if success:
        f = open(files.get_project_root() + "/logs/log_success.jsonl", "a")
    else:
        f = open(files.get_project_root() + "/logs/log_fail.jsonl", "a")
    log = args
    f.write(json.dumps(log) + "\n")
    f.close()
