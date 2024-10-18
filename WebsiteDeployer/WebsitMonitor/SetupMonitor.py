import logging
import threading
import time
from SetLogger import LogSetter
from cli import CLIMenu
from KeyManager.KeyManager import KeyManager
from ServerManager.SSHServer import SSHServer
from ConfigLoader import ConfigLoader
from BackupSystem.Compressor import compress_folder
from WebsitMonitor.DiscordNotifier import discord_notifier_interface, DiscordNotifier
from Models import *
from Pinger import ping_target


def ping_loop(webserver: Webserver):
    bot = DiscordNotifier(
        webserver
    )
    discord_notifier_interface("start", bot)
    while ping_target(webserver.url):
        print("pinged")
        time.sleep(30)

    discord_notifier_interface("notify_user", bot)

def main():
    # Change Paramiko logging level to Warning
    logging.getLogger("paramiko").setLevel(logging.WARNING)

    logger = LogSetter(logging.DEBUG)
    logger.setup()

    logging.debug("loading configurations...")
    # Example usage
    loader = ConfigLoader(
        ["../config/webservers.json", "../config/deployer.json"],
        [Webserver, Deployer]  # Changed ConfigLoader to DeployerConfig
    )

    config = loader.load_configs()
    print(config.webserver)

    threads = []
    for server in config.webserver:
        thread = threading.Thread(target=lambda: ping_loop(server))
        thread.start()
        thread.join()
        threads.append(thread)


main()