import binascii
import sys
from ErrorHandler import FatalErrorHandler
import paramiko
import logging
from hashlib import sha3_512
from .Connection import Connection


class SSHServer:
    def __init__(self, hostname, port, username, private_key):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.private_key = private_key

    def connect(self):
        """
        Connects to an SSH server with key file
        :return: Connection instance
        """
        try:
            # Create SSHClient instance
            ssh_client = paramiko.SSHClient()

            # Automatically add the server's host key
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Load the private key (PPK file)
            priv_key = paramiko.RSAKey.from_private_key_file(self.private_key)

            # Connect to the server
            ssh_client.connect(self.hostname, self.port, username=self.username, pkey=priv_key)
            logging.info(f"Connected to {self.hostname}:{self.port}")

            connection = Connection(ssh_client)

            # return connection
            return connection
        except paramiko.SSHException as sshe:
            fatal_handler = FatalErrorHandler.FatalError(sshe, f"SSH Exception occurred while connecting"
                                                               f" to {self.hostname}")
            fatal_handler.display_error()
        except Exception as e:
            fatal_handler = FatalErrorHandler.FatalError(e, f"Exception occurred while connecting"
                                                               f" to {self.hostname}")
            fatal_handler.display_error()

    def disconnect(self, connection):
        """
        Disconnects from SSH server by closing connection
        :param connection: Connection instance
        """
        try:
            logging.debug(f"Disconnecting from {self.hostname}:{self.port}...")
            if connection.sftp_con:
                connection.sftp_con.close()
                logging.debug("SFTP connection closed")
            if connection.ssh_con:
                connection.ssh_con.close()
                logging.debug("SSH connection closed")
        except paramiko.ssh_exception.SSHException as ssh_exception:
            logging.warning("An SSH exception occurred while closing connection:", ssh_exception)
        except Exception as e:
            logging.warning("An error occurred while closing the connection:", e)

    def verify_server_identity(self, conn: paramiko.SSHClient, fingerprint_from_keystore):
        """
        Verify server identity by comparing fingerprint from keystore with the provided one
        :param conn: paramiko.SSHClient instance
        :param fingerprint_from_keystore: fingerprint from Data/keystore.json
        :return: True if the server identity is valid, False if not
        """
        logging.debug("Verifying server identity...")

        def hash_sha3_512(input_str):
            try:
                f_hash = sha3_512()
                f_hash.update(str(input_str).encode())
                return f_hash.hexdigest()
            except Exception as hash_e:
                print(f'Error hashing fingerprint: {hash_e}')

        try:
            # Get transport object
            transport_object = conn.get_transport()
            # Get host key from transport object
            host_key = transport_object.get_remote_server_key()
            # Get fingerprint from host_key (MD5 hash host key)
            md5_fingerprint = host_key.get_fingerprint()

            # Decode and get the hexadecimal value of the fingerprint
            server_provided_fingerprint_hex = binascii.hexlify(md5_fingerprint).decode('utf-8')

            # Compare fingerprints
            if hash_sha3_512(server_provided_fingerprint_hex) == fingerprint_from_keystore:
                logging.debug("Fingerprint match. Connection is secure")
                return True
            else:
                logging.critical("Fingerprints does not match. Connection is insecure. Closing connection...")
                conn.close()
                logging.debug(f"Disconnected from {self.hostname}:{self.port}")
                sys.exit()

        except Exception as e:
            logging.critical(f"Error while verifying server identity: {e}")
