import pick
import logging


class CLIMenu:
    def __init__(self):
        self.current_menu = "Main Menu"
        self.indicator = "->"

    def main_menu(self):
        selected = ""
        while selected != "Exit":
            options = ["Deploy Server", "Rollback", "Exit"]
            selected, index = pick.pick(options, "Main Menu [ CLI root ]", indicator=self.indicator, default_index=0)
            match selected:
                case "Deploy Server":
                    pass
                case "Rollback":
                    pass
                case "Exit":
                    return

