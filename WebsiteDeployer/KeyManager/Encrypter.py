from cryptography.fernet import Fernet
import logging
from ErrorHandler import FatalErrorHandler


def encrypt_file(input_file, output_file, encryption_key):
    fernet = Fernet(encryption_key)
    try:
        with open(input_file, "rb") as file_v:
            data = file_v.read()
            encrypted_data = fernet.encrypt(data)
        with open(output_file, "wb") as file_v:
            file_v.write(encrypted_data)
    except FileNotFoundError as fnf:
        logging.critical(f"File not found: {input_file}")
        fatal_handler = FatalErrorHandler.FatalError(fnf, f"File not found: {input_file}")
        fatal_handler.display_error()
    except Exception as e:
        logging.critical(f"Error encrypting the file: {str(e)}.\nThis means that the ssh key file is in plain text!")
        fatal_handler = FatalErrorHandler.FatalError(e, f"Error encrypting the file.\n"
                                                        f"This means that the ssh key file is in plain text!")
        fatal_handler.display_error()


def decrypt_file(input_file, output_file, encryption_key):
    fernet = Fernet(encryption_key)
    try:
        with open(input_file, "rb") as file_v:
            encrypted_data = file_v.read()
            decrypted_data = fernet.decrypt(encrypted_data)
        with open(output_file, "wb") as file_v:
            file_v.write(decrypted_data)
    except FileNotFoundError as fnf:
        fatal_handler = FatalErrorHandler.FatalError(fnf, f"File not found.")
        fatal_handler.display_error()
    except Exception as e:
        fatal_handler = FatalErrorHandler.FatalError(e, f"Error decrypting file.")
        fatal_handler.display_error()
