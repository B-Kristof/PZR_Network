import logging
from .SendCommand import execute_command
from ServerManager.Connection import Connection
from ConfigLoader import *


def compress_folder(conn: Connection, config: Config):
    """
    Compress webserver_folder on server side specified in config/deployer.json to backup_folder
    also specified in config/deployer.json
    :param conn: Connection instance
    :param config: Config instance
    :return: True on success
    """
    logging.debug(f"Compressing webserver folder ({config.deployer.webserver_folder}) on server side...")
    compress_command = (
        f"tar -cvf"
        f" {config.deployer.backup_folder}/PZRWebsiteBackup.tar "
        f"{config.deployer.webserver_folder}"
                        )
    execute_command(conn, compress_command)

    return True
