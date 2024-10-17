import logging
from SetLogger import LogSetter
from cli import CLIMenu
from KeyManager.KeyManager import KeyManager
from ServerManager.SSHServer import SSHServer
from ConfigLoader import load_config, DeployerConfig
from BackupSystem.Compressor import compress_folder


if __name__ == "__main__":

    # Change Paramiko logging level to Warning
    logging.getLogger("paramiko").setLevel(logging.WARNING)

    logger = LogSetter(logging.DEBUG)
    logger.setup()

    '''
    logging.debug("Requesting CLI startup...")
    cli = CLIMenu()
    cli.main_menu()
    '''
    keymanager = KeyManager("Data/keystore.json", "Data/ssh-key-server.key")
    sshserver = SSHServer("pzrteam.hu", 22, "ubuntu", "Data/ssh-key-server.key")
    conn = sshserver.connect()
    sshserver.verify_server_identity(conn.ssh_con, keymanager.load_fingerprint())
    conn.extend_to_sftp()

    logging.debug("loading Deployer configuration...")
    deployer_config: DeployerConfig = load_config("config/deployer.json")
    if deployer_config:
        logging.debug(f"\nDeployer configuration parameters:\nWebserver folder: {deployer_config.webserver_folder}\n"
                      f"Backup folder: {deployer_config.backup_folder}")
    else:
        raise Exception("Invalid or missing deployer configuration file!")

    compress_folder(conn, deployer_config)



