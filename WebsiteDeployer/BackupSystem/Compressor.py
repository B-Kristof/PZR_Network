from ErrorHandler import NonFatalErrorHandler
from Models import Webserver
from ServerManager.SendCommand import execute_command
from ServerManager.SSHServer import SSHServerConnection
from ConfigLoader import *
from .PromptSkipBackup import prompt_skip_backup


def check_remote_dir_exists(conn: SSHServerConnection, folder: str):
    """
    Check if Remote Folder / Directory exists on server side
    :param conn: Connection instance
    :param folder: Folder to check
    :return: True if exists, false if not
    """
    try:
        return bool(execute_command(conn.ssh_con, f"test -d {folder} && echo true || echo false"))
    except Exception as e:
        fatal_handler = FatalErrorHandler.FatalError(e, "Backup could not be created!")
        fatal_handler.display_error()


def compress_folder(webserver: Webserver):
    """
    Compress webserver_folder on server side specified in webserver.json
    also specified in config/webserver.conf
    :param webserver: Webserver instance
    :return: True on success
    """
    try:
        logging.debug(f"Compressing webserver folder ({webserver.webserver_folder}) on server side...")
        compress_command = (
            f"sudo tar -cvf"
            f" {webserver.remote_backup_path} "
            f"{webserver.webserver_folder}"
        )
        output = execute_command(webserver.conn, compress_command)

        if not output:
            if (input("WARNING: Backup was not created due to an exception. This means that ALL of the current "
                      "files will be OVERWRITTEN. Do you want to continue with the deployment? (y or n)" == "n")):
                e = Exception("Backup could not be created. Abort by user!")
                fatal_handler = FatalErrorHandler.FatalError(e, "Backup could not be created!")
                fatal_handler.display_error()

        return True

    except Exception as e:
        error_handler = NonFatalErrorHandler.NonFatalError(e, "Error occurred while compressing folder "
                                                              "on server side")
        error_handler.display_error()
        prompt_skip_backup()
        return False