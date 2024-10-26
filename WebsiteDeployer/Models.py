import datetime
import logging
import socket
from KeyManager.KeyManager import KeyManager
from ServerManager.SSHServer import SSHServerConnection


class DiscordBot:
    def __init__(self, token: str, user_id: int):
        self.token = token
        self.user_id = user_id


class Deployer:
    def __init__(self, webserver_folder: str, backup_folder: str):
        self.webserver_folder = webserver_folder
        self.backup_folder = backup_folder


class Webserver:
    def __init__(self, url: str, ip_address: str, role: str, state: bool, last_answer: datetime.datetime,
                 webserver_folder: str, remote_backup_path: str, local_backup_path: str, local_folder: str, ssh_key_file: str):
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
        self.conn = None # False if offline
        self.sftp_con = None # False if offline

    def connect(self):
        """
        Create SSH connection to a server
        """
        if self.ping_ip():
            # Server is up
            keymanager = KeyManager("Data/keystore.json", self.ssh_key_file)
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

    def change_state(self, new_state: bool):
        """
        Change state attribute
        :param new_state: New state
        """
        self.state = new_state
