import os
import sys
from datetime import datetime
from .Compressor import compress_folder
from BackupSystem.PromptSkipBackup import prompt_skip_backup
from ServerManager.TransferManager import *
from Models import Webserver
from ErrorHandler import FatalErrorHandler, NonFatalErrorHandler
from .IntegrityChecker import check_backup_integrity

def generate_file_suffix():
    """
    Returns the current date and time in the format YYYY_MM_DD_HH_MM_SS.
    """
    now = datetime.now()
    formatted_datetime = now.strftime("%Y_%m_%d_%H_%M_%S")
    return "_" + str(formatted_datetime) + ".tar"

def ensure_path_and_check_folders(path):
    """
    Ensure the specified path exists, and check if all items in the path are folders.

    :param path: The path to check or create.
    :return: True if the path exists and all items in it are folders, False otherwise.
    """
    # Create the path if it doesn't exist
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            logging.info(f"Path '{path}' created.")
            return True
        except PermissionError as pe:
            error_handler = NonFatalErrorHandler.NonFatalError(pe, "Permission Error.Could not create folders to save backup")
            error_handler.display_error()
            prompt_skip_backup()
            return False
        except Exception as e:
            error_handler = NonFatalErrorHandler.NonFatalError(e, "Error: Could not create folders to save backup")
            error_handler.display_error()
            prompt_skip_backup()
            return False

    else:
        return True


def create_backup(webserver: Webserver):
    """
    Create backup of the website
    :param webserver: Webserver instance
    :return: True if backup created, False otherwise
    """
    try:
        compress_res = compress_folder(webserver)

        folders = webserver.local_backup_path.split("/")
        folders.remove(folders[-1])
        local_backup_folder = "\\".join(map(str, folders))
        local_backup_file_name = webserver.local_backup_path.removesuffix(".tar") + generate_file_suffix()
        if ensure_path_and_check_folders(local_backup_folder) and compress_res:
            download_file_sftp(
                webserver,
                webserver.remote_backup_path,
                local_backup_file_name
            )

            if not check_backup_integrity(webserver, local_backup_file_name, webserver.remote_backup_path):
                prompt_skip_backup()
            else:
                logging.info("Backup created successfully.")
        else:
            return False
    except Exception as e:
        nonfatal_handler = NonFatalErrorHandler.NonFatalError(e, "Error: Cannot download backup file.")
        nonfatal_handler.display_error()
        print("WARNING: Backup was not created due to an exception. "
              "This means that ALL of the current files will be OVERWRITTEN and you have no up to date backup.")
        if input("Do you want to continue? (y or n)" == "n"):
            sys.exit()

