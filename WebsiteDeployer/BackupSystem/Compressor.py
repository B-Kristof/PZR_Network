import logging
from .SendCommand import execute_command
from ServerManager.Connection import Connection
from ConfigLoader import DeployerConfig


def compress_folder(conn: Connection, deployer_config: DeployerConfig):
    """
    Compress webserver_folder on server side specified in config/deployer.json to backup_folder
    also specified in config/deployer.json
    :param conn: Connection instance
    :param deployer_config: DeployerConfig instance
    :return: True on success
    """
    logging.debug(f"Compressing webserver folder ({deployer_config.webserver_folder}) on server side...")
    compress_command = (
        f"tar -cvf"
        f" {deployer_config.backup_folder}/PZRWebsiteBackup.tar "
        f"{deployer_config.webserver_folder}"
                        )
    execute_command(conn, compress_command)

    return True
