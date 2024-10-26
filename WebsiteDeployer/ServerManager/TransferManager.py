import logging
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