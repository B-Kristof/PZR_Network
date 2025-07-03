import datetime
import logging
import os.path
import shutil
import socket
import pysftp
from clr_loader.util import path_as_string

from src.KeyManager.KeyManager import KeyManager
from src.ServerManager.SSHServer import SSHServerConnection
from src.ServerManager.SendCommand import execute_command
from src.BackupSystem.Compressor import compress_local_folder


class Webserver:
    def __init__(self, url: str, ip_address: str, role: str, state: bool, last_answer: datetime.datetime,
                 webserver_folder: str, remote_backup_path: str, local_backup_path: str, local_folder: str,
                 ssh_key_file: str, to_deploy: list[str]):
        self.is_valid = False
        self.invalid_reason = None
        self.url = url
        self.ip_address = ip_address
        self.role = role
        self.state = state
        self.last_answer = last_answer
        self.webserver_folder = webserver_folder
        self.remote_backup_path = remote_backup_path
        self.local_backup_path = local_backup_path
        self.local_folder = local_folder
        self.ssh_key_file = ssh_key_file
        self.conn = None  # False if offline
        self.sftp_con = None  # False if offline
        self.to_deploy = to_deploy

    def __str__(self):
        attributes = ""
        for attr in self.__dict__:
            attributes += f"{attr}: {getattr(self, attr)}\n"

        return attributes

    def initialize(self):
        """
        Initialize the webserver instance
        """
        # Checking initial server state
        reason = ""
        logging.debug(f"Initializing webserver {self.url} ({self.ip_address})...")
        self.state = self.ping_ip()
        if self.state:
            logging.info(f"{self.url} is up.")
        else:
            logging.warning(f"Server {self.ip_address} is down.")
            reason += " Server is down."

        # Create Connection
        self.connect()

        # Create SFTP connection
        if self.conn:
            self.extend_to_sftp()
        else:
            logging.error("Connection to server failed. SFTP connection not established.")
            reason += " Cannot establish connection to server."

        # Checking paths on local machine
        if not os.path.exists(self.local_folder):
            logging.error(f"Local folder {self.local_folder} does not exist.")
            reason += " Local folder does not exist."
        if not os.path.exists(self.ssh_key_file):
            logging.error(f"SSH key file {self.ssh_key_file} does not exist.")
            reason += " SSH key file does not exist."

        # Checking paths on remote machine
        if self.send_command(f'if [ -d "{self.webserver_folder}" ]; then echo "Folder exists"; else echo "Folder does'
                             f' not exist"; fi') == "Folder does not exist":
            logging.error(f"Webserver folder {self.webserver_folder} does not exist on server side.")
            reason += " Webserver folder does not exist on server side."

        if not reason:
            logging.debug(f"Webserver {self.url} ({self.ip_address}) initialized.")
            self.is_valid = True
            return True
        else:
            self.invalid_reason = reason
            logging.error(f"Webserver {self.url} ({self.ip_address}) is not initialized: {self.invalid_reason}")
            return False

    def connect(self):
        """
        Create SSH connection to a server
        """
        if self.ping_ip():
            # Server is up
            keymanager = KeyManager("src/Data/keystore.json", self.ssh_key_file)
            sshserver = SSHServerConnection(self.ip_address, 22, "ubuntu", self.ssh_key_file)
            conn = sshserver.connect()
            sshserver.verify_server_identity(keymanager.load_fingerprint())
            self.conn = conn
        else:
            # Server is down
            self.conn = False
            self.sftp_con = False

    def ping_ip(self, port=22, timeout=2):
        """
        Ping a server
        :param port: port to ping
        :param timeout: timeout in ms
        :return: True if server is up, False if server is down
        """
        try:
            with socket.create_connection((self.ip_address, port), timeout=timeout):
                logging.info(f"{self.ip_address} ({self.url}) is up.")
                return True
        except (socket.timeout, socket.error):
            logging.info(f"{self.ip_address} ({self.url}) is down.")
            return False

    def send_command(self, command: str):
        """
        Send command to server
        :param command: command to send
        :return: output of the command
        """
        if self.conn or not self.is_valid:
            return execute_command(self.conn, command)
        else:
            logging.error(f"Connection to {self.url} ({self.ip_address}) is not established or the webserver config is invalid.")
            return False

    def put_folder(self, local_compressed_folder_or_file: str, remote_path: str):
        


    def extend_to_sftp(self):
        """
        Extend SSH connection to SFTP
        """
        self.sftp_con = self.conn.extend_to_sftp()

    def change_last_answer(self, new_last_answer: datetime.datetime):
        """
        Change last answer attribute
        :param new_last_answer: new last answer
        """
        self.last_answer = new_last_answer

