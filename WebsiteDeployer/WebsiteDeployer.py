import logging
import threading
from SetLogger import LogSetter
from cli import CLIMenu
from KeyManager.KeyManager import KeyManager
from ServerManager.SSHServer import SSHServer
from ConfigLoader import ConfigLoader
from BackupSystem.Compressor import compress_folder
from WebsitMonitor.DiscordNotifier import discord_notifier_interface, DiscordNotifier
from Models import *
from ErrorHandler.FatalErrorHandler import *
from ErrorHandler.KeyboardInterruptHandler import *
from ErrorHandler import CleanUpHandler


if __name__ == "__main__":
    conn, ssh_server = None, None


    try:
        # Change Paramiko logging level to Warning
        logging.getLogger("paramiko").setLevel(logging.WARNING)

        logger = LogSetter(logging.DEBUG)
        logger.setup()

        logging.debug("loading configurations...")
        # Example usage
        loader = ConfigLoader(
            ["config/webservers.json", "config/deployerasd.json"],
            [Webserver, Deployer]  # Changed ConfigLoader to DeployerConfig
        )

        config = loader.load_configs()

    except KeyboardInterrupt as kbi_exception:
        kbi_handler = KeyboardInterruptHandler(kbi_exception)
        kbi_handler.display_error()
    finally:
        CleanUpHandler.cleanup(ssh_server, conn)

    '''
    # Prompt to select webserver
    logging.debug("Requesting CLI startup...")
    cli = CLIMenu(config)
    cli.main_menu()

    keymanager = KeyManager("Data/keystore.json", "Data/ssh-key-server.key")
    sshserver = SSHServer("pzrteam.hu", 22, "ubuntu", "Data/ssh-key-server.key")
    conn = sshserver.connect()
    sshserver.verify_server_identity(conn.ssh_con, keymanager.load_fingerprint())
    conn.extend_to_sftp()
    '''


