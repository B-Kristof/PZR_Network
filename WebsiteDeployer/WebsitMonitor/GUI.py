import tkinter as tk
import logging
from ServerManager.Connection import Connection
from ErrorHandler import FatalErrorHandler
from ConfigLoader import Config
from WebsitMonitor import Pinger
from Models import Webserver


class GUIElement:
    def __init__(self, element, ws: Webserver or None):
        self.element = element
        self.ws = ws

    def place_element(self, x: int, y: int):
        """
        Place a GUIElement on the grid
        """
        self.element.grid(column=x, row=y)


class GUIStateIndicator(GUIElement):
    def __init__(self, element, ws: Webserver):
        super().__init__(element, ws)
        element.config(fg="green")

    def set_state(self, new_state):
        self.element.config(text=new_state)
        self.element.config(fg="red" if new_state == "down" else "green")


class GUILabel(GUIElement):
    def __init__(self, element, ws: Webserver):
        super().__init__(element, ws)


class MainWindow:
    def __init__(self, conn: Connection, config: Config):
        self.conn = conn
        self.config = config
        self.root = tk.Tk()
        self.x = 0
        self.y = 0
        self.indicators = []

        self.root.after(10000, self.run_pinger)

    def open(self):
        """
        open Main Window
        :return:
        """
        logging.debug("Root window opened")
        self.build_gui()
        self.root.mainloop()

    def run_pinger(self):
        for ws in self.config.webserver:
            current_indicator = None
            response = Pinger.ping_target(ws.url)
            for indicator in self.indicators:
                current_indicator = indicator
            if response and not current_indicator.ws.state:
                current_indicator.set_state("up")
            elif response and current_indicator.ws.state:
                current_indicator.set_state("down")

        # Schedule the pinger to run again after 10 seconds
        self.root.after(10000, self.run_pinger)

    def build_gui(self):
        for ws in self.config.webserver:
            ws_label = GUILabel(tk.Label(text=ws.url), ws)
            ws_indicator = GUIStateIndicator(tk.Label(text="up" if ws.state else "down"), ws)
            ws_label.place_element(self.x, self.y)
            self.x += 1
            ws_indicator.place_element(self.x, self.y)
            self.indicators.append(ws_indicator)
            self.y += 1
            self.x -= 1

