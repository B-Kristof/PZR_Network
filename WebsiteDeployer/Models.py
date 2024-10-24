import datetime


class DiscordBot:
    def __init__(self, token: str, user_id: int):
        self.token = token
        self.user_id = user_id


class Deployer:
    def __init__(self, webserver_folder: str, backup_folder: str):
        self.webserver_folder = webserver_folder
        self.backup_folder = backup_folder


class Webserver:
    def __init__(self, url: str, ip_address: str, role: str, state: bool, last_answer: datetime.datetime):
        self.url = url
        self.ip_address = ip_address
        self.role = role
        self.state = state
        self.last_answer = last_answer

    def change_last_answer(self, new_last_answer: datetime.datetime):
        self.last_answer = new_last_answer

    def change_state(self, new_state: bool):
        self.state = new_state
