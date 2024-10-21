import logging
from ServerManager.SSHServer import SSHServer
from ServerManager.Connection import Connection


def cleanup(ssh_server: SSHServer or None, conn: Connection or None):
    """
    Close SSH and SFTP connection and hang the program until user input
    :param ssh_server: SSHServer instance
    :param conn: Connection Instance
    """
    logging.debug("Starting cleanup...")
    if ssh_server:
        ssh_server.disconnect(conn)
    else:
        logging.debug("No connection to close!")

    input("Press any key to exit...")