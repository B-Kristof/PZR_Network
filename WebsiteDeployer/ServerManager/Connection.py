import logging
import paramiko


class Connection:
    def __init__(self, ssh_client: paramiko.SSHClient):
        self.ssh_con = ssh_client
        self.sftp_con = None

    def extend_to_sftp(self):
        self.sftp_con = self.ssh_con.open_sftp()
        logging.info("Extended SSH connection to SFTP.")
