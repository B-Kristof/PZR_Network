import logging
from SetLogger import LogSetter
from cli import CLIMenu
from KeyManager.KeyManager import KeyManager
from ServerManager.SSHServer import SSHServer
from ConfigLoader import ConfigLoader
from BackupSystem.Compressor import compress_folder
from Models import *


if __name__ == "__main__":

    # Change Paramiko logging level to Warning
    logging.getLogger("paramiko").setLevel(logging.WARNING)

    logger = LogSetter(logging.DEBUG)
    logger.setup()

    logging.debug("loading configurations...")
    # Example usage
    loader = ConfigLoader(
        ["config/webservers.json", "config/deployer.json"],
        [Webserver, Deployer]  # Changed ConfigLoader to DeployerConfig
    )

    config = loader.load_configs()

    # Prompt to select webserver
    logging.debug("Requesting CLI startup...")
    cli = CLIMenu(config)
    cli.main_menu()

    '''
    keymanager = KeyManager("Data/keystore.json", "Data/ssh-key-server.key")
    sshserver = SSHServer("pzrteam.hu", 22, "ubuntu", "Data/ssh-key-server.key")
    conn = sshserver.connect()
    sshserver.verify_server_identity(conn.ssh_con, keymanager.load_fingerprint())
    conn.extend_to_sftp()
    '''


