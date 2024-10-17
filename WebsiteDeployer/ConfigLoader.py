import os
import json


class DeployerConfig:
    def __init__(self, webserver_folder: str, backup_folder: str):
        self.webserver_folder = webserver_folder
        self.backup_folder = backup_folder


def load_json(infile_path: str) -> dict or bool:
    """
    :param infile_path: path and json file
    :return: dict or False if failed
    """

    if not os.path.exists(infile_path):
        return False

    try:
        with open(infile_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        return False


def parse_json(json_data) -> 'DeployerConfig' or bool:
    """
    :param json_data: dict object to parse
    :return: DeployerConfig instance or False if failed
    """
    if json_data:
        return DeployerConfig(
            json_data["webserver_folder"],
            json_data["backup_folder"]
        )
    else:
        return False


def load_config(infile_path: str) -> 'DeployerConfig' or bool:
    """
    :param infile_path: path and json file
    :return: DeployerConfig instance or False if failed
    """
    return parse_json(load_json(infile_path))
