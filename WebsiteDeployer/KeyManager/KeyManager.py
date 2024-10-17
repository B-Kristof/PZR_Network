import json
from .Encrypter import *


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
        except FileNotFoundError:
            print(f"File not found: {self.keystore}. This error is fatal!\n\nAbort by system.")
            exit()
        except json.JSONDecodeError as e:
            print(f"Fatal Error decoding JSON ({self.keystore}): {e}\n\nAbort by system.")
            exit()

    def load_fingerprint(self):
        try:
            with open(self.keystore, 'r') as ks:
                data = json.load(ks)
            return data['server_fingerprint']
        except FileNotFoundError:
            print(f"File not found: {self.keystore}. This error is fatal!\n\nAbort by system.")
            exit()
        except json.JSONDecodeError as e:
            print(f"Fatal Error decoding JSON ({self.keystore}): {e}\n\nAbort by system.")
            exit()
