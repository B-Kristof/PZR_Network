import datetime
import logging
import os
import socket
from src.KeyManager.KeyManager import KeyManager
from src.ServerManager.SSHServer import SSHServerConnection


class DiscordBot:
    def __init__(self, token: str, user_id: int):
        self.token = token
        self.user_id = user_id


class Deployer:
    def __init__(self, webserver_folder: str, backup_folder: str):
        self.webserver_folder = webserver_folder
        self.backup_folder = backup_folder