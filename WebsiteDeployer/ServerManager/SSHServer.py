import logging
import paramiko
import binascii
import sys
from ErrorHandler import FatalErrorHandler
from hashlib import sha3_512


class SSHServerConnection:
    def __init__(self, hostname, port, username, private_key):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.private_key = private_key
        self.ssh_con = None
        self.sftp_con = None

    def connect(self):
        """
        Connects to an SSH server using a private key.
        :return: True if the connection is successful, False otherwise
        """
        try:
            # Initialize SSH client and set host key policy
            self.ssh_con = paramiko.SSHClient()
            self.ssh_con.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Load the private key
            priv_key = paramiko.RSAKey.from_private_key_file(self.private_key)

            # Establish the SSH connection
            self.ssh_con.connect(self.hostname, self.port, username=self.username, pkey=priv_key)
            logging.info(f"Connected to {self.hostname}:{self.port}")
            return self
        except paramiko.SSHException as sshe:
            fatal_handler = FatalErrorHandler.FatalError(sshe, f"SSH Exception while connecting to {self.hostname}")
            fatal_handler.display_error()
        except Exception as e:
            fatal_handler = FatalErrorHandler.FatalError(e, f"Exception while connecting to {self.hostname}")
            fatal_handler.display_error()

    def extend_to_sftp(self):
        """
        Extends the SSH connection to an SFTP connection.
        :return: SFTP client instance if successful, None otherwise
        """
        try:
            logging.debug("Extending SSH connection to SFTP...")
            self.sftp_con = self.ssh_con.open_sftp()
            logging.info("SFTP connection established.")
            return self.sftp_con
        except Exception as e:
            fatal_handler = FatalErrorHandler.FatalError(e, "Fatal error while creating SFTP connection")
            fatal_handler.display_error()
            return None

    def verify_server_identity(self, fingerprint_from_keystore):
        """
        Verify server identity by comparing fingerprint from keystore with the server's fingerprint.
        :param fingerprint_from_keystore: Expected fingerprint from keystore.
        :return: True if the server identity is valid, False otherwise.
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
            # Obtain the server's host key and fingerprint
            transport_object = self.ssh_con.get_transport()
            host_key = transport_object.get_remote_server_key()
            md5_fingerprint = host_key.get_fingerprint()
            server_provided_fingerprint_hex = binascii.hexlify(md5_fingerprint).decode('utf-8')

            # Compare the hashed fingerprint with the expected one
            if hash_sha3_512(server_provided_fingerprint_hex) == fingerprint_from_keystore:
                logging.debug("Fingerprint match. Connection is secure")
                return True
            else:
                logging.critical("Fingerprints do not match. Connection is insecure. Closing connection...")
                self.ssh_con.close()
                logging.debug(f"Disconnected from {self.hostname}:{self.port}")
                sys.exit()
        except Exception as e:
            logging.critical(f"Error while verifying server identity: {e}")
        return False

    def disconnect(self):
        """
        Disconnects from the SSH server by closing the connection and the SFTP client if active.
        """
        try:
            logging.debug(f"Disconnecting from {self.hostname}:{self.port}...")
            if self.sftp_con:
                self.sftp_con.close()
                logging.debug("SFTP connection closed")
            if self.ssh_con:
                self.ssh_con.close()
                logging.debug("SSH connection closed")
        except paramiko.ssh_exception.SSHException as ssh_exception:
            logging.warning("An SSH exception occurred while closing connection:", ssh_exception)
        except Exception as e:
            logging.warning("An error occurred while closing the connection:", e)
