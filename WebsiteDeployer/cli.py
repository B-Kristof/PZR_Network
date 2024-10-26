import time

import pick
import logging
from ConfigLoader import Config
from BackupSystem.BackupCreator import create_backup


class CLIMenu:
    def __init__(self, config):
        self.config = config
        self.current_menu = "Main Menu"
        self.indicator = "->"
        self.target_webserver = None

    def main_menu(self):
        selected = ""
        while selected != "Exit":
            title = (
                f"Main Menu [ Target: {self.target_webserver.role} ({self.target_webserver.url}) ]"
                if self.target_webserver
                else "Main Menu [ CLI root ]"
            )

            if not self.target_webserver:
                options = ["Select Webserver", "Exit"]
                selected, index = pick.pick(options, title, indicator=self.indicator, default_index=0)
                match selected:
                    case "Select Webserver":
                        self.set_target_menu()
                    case "Exit":
                        return
            else:
                options = ["Deploy Server", "Create backup", "Rollback", "Back", "Exit"]
                selected, index = pick.pick(options, title, indicator=self.indicator, default_index=0)
                match selected:
                    case "Deploy Server":
                        pass
                    case "Create backup":
                        create_backup(webserver=self.target_webserver)
                        time.sleep(3)
                    case "Rollback":
                        pass
                    case "Back":
                        self.target_webserver = None
                    case "Exit":
                        return

    def set_target_menu(self):
        selected = ""
        while selected != "Exit":
            options = [server.role for server in self.config.webserver]
            selected, index = pick.pick(options, "Select target", indicator=self.indicator, default_index=0)
            if selected in options:
                self.target_webserver = next((s for s in self.config.webserver if s.role == selected), None)
                self.target_webserver.connect()
                self.target_webserver.extend_to_sftp()
                return selected
            else:
                return

