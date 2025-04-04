from SetLogger import LogSetter
from BackupSystem.BackupCreator import create_backup
from ConfigLoader import ConfigLoader
from Models import *
from ErrorHandler.FatalErrorHandler import *
from ErrorHandler.KeyboardInterruptHandler import *
from ErrorHandler import CleanUpHandler

if __name__ == "__main__":
    conn, config, sshserver = None, None, None
    try:
        # Change Paramiko logging level to Warning
        logging.getLogger("paramiko").setLevel(logging.WARNING)

        logger = LogSetter(logging.DEBUG)
        logger.setup()

        logging.debug("loading configurations...")
        loader = ConfigLoader(
            ["config/webservers.json"], # , "config/discordbot.json"
            [Webserver]  #, DiscordBot Changed ConfigLoader to DeployerConfig
        )

        config = loader.load_configs()
        config.webserver[0].connect()
        config.webserver[0].extend_to_sftp()
        # config.webserver[0].map_files()
        # config.webserver[0].deploy_files()

        create_backup(webserver=config.webserver[0])

    except KeyboardInterrupt as kbi_exception:
        kbi_handler = KeyboardInterruptHandler(kbi_exception)
        kbi_handler.display_error()
    except Exception as e:
        fatal_handler = FatalError(e, "Fatal Error")
        fatal_handler.display_error()
    finally:
        CleanUpHandler.cleanup(config)

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


