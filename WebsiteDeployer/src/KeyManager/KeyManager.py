import json
from .Encrypter import *
from ErrorHandler import FatalErrorHandler

class KeyManager:
    def __init__(self, keystore_file, ssh_key_file):
        self.keystore = keystore_file
        self.ssh_key_file = ssh_key_file

    def decrypt(self):
        enc_key = self.load_encryption_key()
        decrypt_file(input_file=self.ssh_key_file, output_file=self.ssh_key_file, encryption_key=enc_key)

    def encrypt(self):
        enc_key = self.load_encryption_key()
        encrypt_file(input_file=self.ssh_key_file, output_file=self.ssh_key_file, encryption_key=enc_key)

    def load_encryption_key(self):
        try:
            with open(self.keystore, 'r') as ks:
                data = json.load(ks)
            return data['encryption_key']
        except FileNotFoundError as fnf:
            fatal_handler = FatalErrorHandler.FatalError(fnf, f"{self.keystore} not found!")
            fatal_handler.display_error()
        except json.JSONDecodeError as jsone:
            fatal_handler = FatalErrorHandler.FatalError(jsone, f"Fatal Error decoding JSON ({self.keystore})")
            fatal_handler.display_error()
        except Exception as e:
            fatal_handler = FatalErrorHandler.FatalError(e, f"Unhandled Fatal exception occurred while"
                                                            f" loading encryption key from keystore")
            fatal_handler.display_error()

    def load_fingerprint(self):
        try:
            with open(self.keystore, 'r') as ks:
                data = json.load(ks)
            return data['server_fingerprint']
        except FileNotFoundError as fnf:
            fatal_handler = FatalErrorHandler.FatalError(fnf, f"{self.keystore} not found!")
            fatal_handler.display_error()
        except json.JSONDecodeError as jsone:
            fatal_handler = FatalErrorHandler.FatalError(jsone, f"Fatal Error decoding JSON ({self.keystore})")
            fatal_handler.display_error()
        except Exception as e:
            fatal_handler = FatalErrorHandler.FatalError(e, f"Unhandled Fatal exception occurred while"
                                                            f" loading fingerprint key from keystore")
            fatal_handler.display_error()
