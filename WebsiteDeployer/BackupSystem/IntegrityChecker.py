import hashlib
import logging
from ErrorHandler import NonFatalErrorHandler
from ServerManager.SendCommand import execute_command
from Models import Webserver


def check_backup_integrity(webserver: Webserver, local_file, remote_file):
    def calculate_file_md5(file_path):
        try:
            md5_hash = hashlib.md5()
            with open(file_path, "rb") as file:
                while True:
                    data = file.read(65536)  # Read the file in 64K chunks
                    if not data:
                        break
                    md5_hash.update(data)
            return md5_hash.hexdigest()
        except FileNotFoundError as e:
            error_handler = NonFatalErrorHandler.NonFatalError(e, f"Error occurred while checking backup "
                                                                  f"file integrity. File not found.")
            error_handler.display_error()
        except PermissionError as e:
            error_handler = NonFatalErrorHandler.NonFatalError(e, f"Permission error occurred while "
                                                                  f"checking backup file integrity")
            error_handler.display_error()
        except IsADirectoryError as e:
            error_handler = NonFatalErrorHandler.NonFatalError(e, f"Error occurred while checking "
                                                                  f"backup file integrity. The specified path is a "
                                                                  f"directory, not a file.")
            error_handler.display_error()
        except Exception as e:
            error_handler = NonFatalErrorHandler.NonFatalError(e, f"Unexpected error occurred while "
                                                                  f"checking backup file integrity.")
            error_handler.display_error()

    # Execute the checksum command on the remote server
    logging.debug('Calculating backup file checksum on remote server...')
    checksum_command = f"md5sum {remote_file}"
    out = execute_command(webserver.conn, checksum_command)
    checksum_result = out.strip().split()[0]

    # Check the integrity of the transferred file
    logging.debug('Calculating local backup file checksum...')
    if checksum_result == calculate_file_md5(local_file):
        logging.info("Checksum values match! Backup file integrity is intact.")
        return True
    else:
        logging.warning("Checksum values does not match! The file may be corrupted.")
        return False
