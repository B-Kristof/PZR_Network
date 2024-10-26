from Models import Webserver
from .SendCommand import execute_command
from ServerManager.Connection import Connection
from ConfigLoader import *


def check_dir_exists(conn: Connection, folder: str):
    out = execute_command(conn, f"test -d {folder} && echo true || echo false")
    print(type(bool(out)))


def compress_folder(conn: Connection, webserver: Webserver):
    """
    Compress webserver_folder on server side specified in config/deployer.json to backup_folder
    also specified in config/deployer.json
    :param conn: Connection instance
    :param webserver: Webserver instance
    :return: True on success
    """
    logging.debug(f"Compressing webserver folder ({webserver.webserver_folder}) on server side...")
    compress_command = (
        f"tar -cvf"
        f" {webserver.backup_path} "
        f"{webserver.webserver_folder}"
                        )
    output = execute_command(conn, compress_command)

    if not output:
        if (input("WARNING: Backup was not created due to an exception. This means that ALL of the current "
                  "files will be OVERWRITTEN. Do you want to continue with the deployment? (y or n)" == "n")):
            e = Exception("Backup could not be created. Abort by user!")
            fatal_handler = FatalErrorHandler.FatalError(e, "Backup could not be created!")
            fatal_handler.display_error()

    return True
