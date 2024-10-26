import logging
from ConfigLoader import Config


def cleanup(config: Config or None):
    """
    Close SSH and SFTP connection and hang the program until user input
    :param config: Config instance
    """
    logging.debug("Starting cleanup...")
    if config:
        for webserver in config.webserver:
            if webserver.conn:
                webserver.conn.disconnect()
                logging.debug(f"Disconnected from {webserver.ip_address} ({webserver.url})")
            else:
                logging.debug(f"No connection with {webserver.ip_address} ({webserver.url})")
    else:
        logging.debug(f"No connection to close.")

    input("Press any key to exit...")