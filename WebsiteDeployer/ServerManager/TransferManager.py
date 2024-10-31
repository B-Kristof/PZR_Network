import logging
import os
from .SendCommand import execute_command
from ErrorHandler import FatalErrorHandler
from Models import Webserver

def download_file_sftp(webserver: Webserver, remote_file, local_file):
    """
    Downloads a single file from a remote SFTP server to a local file.
    :param webserver: Webserver instance.
    :param remote_file: Path to the remote file to download.
    :param local_file: Path to the local file where the file will be saved.
    """
    try:
        logging.debug(f"Downloading {remote_file} to {local_file}...")
        webserver.sftp_con.get(remote_file, local_file)
        logging.debug("Download complete.")
    except Exception as e:
        fatal_handler = FatalErrorHandler.FatalError(e, f"Fatal error while downloading {remote_file}!")
        fatal_handler.display_error()


def local_file_mapper(local_project_root: str):
    files = []
    for root, _, filenames in os.walk(local_project_root):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            files.append(full_path)

    return files

def remote_file_mapper(conn, remote_project_root: str):
    files = []
    out = execute_command(conn=conn, command=f"find {remote_project_root} -type f")
    for filename in out.splitlines():
        files.append(filename)

    return files
