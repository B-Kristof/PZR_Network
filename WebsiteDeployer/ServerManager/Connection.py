import logging
import paramiko


class Connection:
    def __init__(self, ssh_client: paramiko.SSHClient):
        self.ssh_con = ssh_client
        self.sftp_con = None

    def extend_to_sftp(self):
        logging.debug("Extending SSH connection to SFTP...")
        self.sftp_con = self.ssh_con.open_sftp()
        logging.info("SFTP connection established.")
