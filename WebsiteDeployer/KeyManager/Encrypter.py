from cryptography.fernet import Fernet
import logging


def encrypt_file(input_file, output_file, encryption_key):
    fernet = Fernet(encryption_key)
    try:
        with open(input_file, "rb") as file_v:
            data = file_v.read()
            encrypted_data = fernet.encrypt(data)
        with open(output_file, "wb") as file_v:
            file_v.write(encrypted_data)
    except FileNotFoundError:
        logging.critical(f"File not found: {input_file}")
        exit()
    except Exception as e:
        logging.critical(f"Error encrypting the file: {str(e)}.\nThis means that the ssh key file is in plain text!")
        exit()


def decrypt_file(input_file, output_file, encryption_key):
    fernet = Fernet(encryption_key)
    try:
        with open(input_file, "rb") as file_v:
            encrypted_data = file_v.read()
            decrypted_data = fernet.decrypt(encrypted_data)
        with open(output_file, "wb") as file_v:
            file_v.write(decrypted_data)
    except FileNotFoundError:
        print(f"File not found: {input_file}. This error is fatal!\n\nAbort by system.")
        exit()
    except Exception as e:
        print(f"Error decrypting the file: {str(e)}. This error is fatal!\n\nAbort by system.")
        exit()
