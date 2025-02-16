from SetLogger import LogSetter
from KeyManager.KeyManager import KeyManager
from ServerManager.SSHServer import SSHServer
from ConfigLoader import ConfigLoader
from Models import *
from ErrorHandler.FatalErrorHandler import *
from ErrorHandler.KeyboardInterruptHandler import *
from ErrorHandler import CleanUpHandler
from WebsiteMonitor.GUI import MainWindow

if __name__ == "__main__":
    conn, sshserver = None, None
    try:
        # Change Paramiko logging level to Warning
        logging.getLogger("paramiko").setLevel(logging.WARNING)

        logger = LogSetter(logging.DEBUG)
        logger.setup()

        logging.debug("loading configurations...")
        loader = ConfigLoader(
            ["config/webservers.json", "config/discordbot.json"],
            [Webserver, DiscordBot]  # Changed ConfigLoader to DeployerConfig
        )

        config = loader.load_configs()

        keymanager = KeyManager("Data/keystore.json", "Data/ssh-key-server.key")
        sshserver = SSHServer("pzrteam.hu", 22, "ubuntu", "Data/ssh-key-server.key")
        conn = sshserver.connect()
        sshserver.verify_server_identity(conn.ssh_con, keymanager.load_fingerprint())
        conn.extend_to_sftp()

        main_window = MainWindow(conn, config)
        main_window.open()

    except KeyboardInterrupt as kbi_exception:
        kbi_handler = KeyboardInterruptHandler(kbi_exception)
        kbi_handler.display_error()
    except Exception as e:
        fatal_handler = FatalError(e, "Fatal Error")
        fatal_handler.display_error()
    finally:
        CleanUpHandler.cleanup(sshserver, conn)

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


