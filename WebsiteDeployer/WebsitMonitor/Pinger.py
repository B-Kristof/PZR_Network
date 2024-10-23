import logging
from ErrorHandler import FatalErrorHandler
import requests
from Models import Webserver


def ping_target(target: str, timeout=2):
    """
    Check if a website is up based on the Status code
    :param target: Target website URL
    :param timeout: timeout in ms
    :return: True if Status code is 200, False if not
    """
    try:
        response = requests.get(target, timeout=timeout)
        if response.status_code == 200:
            return True
        else:
            logging.debug(f"{target} answered with status code {response.status_code}")
            return False
    except requests.exceptions.ConnectTimeout:
        logging.debug(f"{target} Timed out.")
        return False
    except Exception as e:
        fatal_handler = FatalErrorHandler.FatalError(e, "Fatal Error while website availability check.")
        fatal_handler.display_error()


def ping_targets(webservers: list[Webserver]):
    """
    Loop over the Webserver instances and check if they are up
    :param webservers: Webserver instance
    """
    for webserver in webservers:
        if ping_target(webserver.url):
            webserver.state = True
        else:
            webserver.state = False
