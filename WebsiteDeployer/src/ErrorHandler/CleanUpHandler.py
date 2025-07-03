import logging
from src.Models.Webserver import Webserver


def cleanup(webservers: list[Webserver]):
    """
    Close SSH and SFTP connection and hang the program until user input
    :param webservers: webserver instances
    """
    logging.debug("Starting cleanup...")
    if webservers:
        for webserver in webservers:
            if webserver.conn:
                webserver.conn.disconnect()
                logging.debug(f"Disconnected from {webserver.url} ({webserver.ip_address})")
            else:
                logging.debug(f"No connection with {webserver.url} ({webserver.ip_address})")
    else:
        logging.debug(f"No connection to close.")

    input("Press any key to exit...")