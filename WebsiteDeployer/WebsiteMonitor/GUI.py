import subprocess
import tkinter as tk
import logging
from ServerManager.Connection import Connection
from ErrorHandler import FatalErrorHandler
from ConfigLoader import Config
from WebsiteMonitor import Pinger
from Models import *


class GUIElement:
    def __init__(self, element, ws: Webserver or None):
        self.element = element
        self.ws = ws
        element.config(bg="black", fg="white")

    def place_element(self, x: int, y: int):
        """
        Place a GUIElement on the grid
        """
        self.element.grid(column=x, row=y, sticky="nsew")


class GUIStateIndicator(GUIElement):
    def __init__(self, element, ws: Webserver):
        super().__init__(element, ws)
        element.config(fg="green" if element.cget("text") == "up" else "red")  # Set initial color

    def set_state(self, new_state):
        self.element.config(text=new_state)
        self.element.config(fg="red" if new_state == "down" else "green")


class GUILabel(GUIElement):
    def __init__(self, element, ws: Webserver or None):
        super().__init__(element, ws)


class MainWindow:
    def __init__(self, conn: Connection, config: Config):
        self.conn = conn
        self.config = config
        self.root = tk.Tk()
        self.root.geometry()
        self.root.configure(bg='black')
        self.header_font = 'Helvetica 10 bold'
        self.x = 0
        self.y = 0
        self.indicators = []
        self.matrix_grid = []

        self.root.after(10000, self.run_pinger)

    def open(self):
        """
        open Main Window
        :return:
        """
        self.generate_matrix_gui()
        self.display_matrix()
        self.root.mainloop()

    def run_pinger(self):
        for ws in self.config.webserver:
            current_indicator = None
            response = Pinger.ping_target(ws.url)
            for indicator in self.indicators:
                if indicator.ws == ws:
                    current_indicator = indicator
                    if response and not current_indicator.ws.state:
                        current_indicator.ws.state = True
                        current_indicator.set_state("up")
                    elif not response and current_indicator.ws.state:
                        current_indicator.ws.state = False
                        current_indicator.set_state("down")
                        self.notify_user_discord(ws)

        # Schedule the pinger to run again after 10 seconds
        self.root.after(10000, self.run_pinger)

    def notify_user_discord(self, webserver: Webserver):
        # Build the command with required arguments
        cmd = [
            'python', 'WebsiteMonitor\\discord_bot.py',
            '--token', self.config.discordbot.token,
            '--user-id', str(self.config.discordbot.user_id),
            '--command', "notify_user"
        ]

        # Add optional arguments if provided
        if webserver.role and webserver.url:
            cmd.extend(['--role', webserver.role, '--url', webserver.url])

        # Call the script
        try:
            logging.debug("Requesting Discord Bot to send message...")
            result = subprocess.run(cmd, check=True, text=True, capture_output=True)
            logging.debug("Message sent!")
        except subprocess.CalledProcessError as e:
            logging.warning(f"Error while sending message: {e.stderr}")

    def generate_matrix_gui(self):
        # Headers
        self.matrix_grid.append(
            [
                GUILabel(tk.Label(self.root, text="Role", font=self.header_font), None),
                GUILabel(tk.Label(self.root, text="URL", font=self.header_font), None),
                GUILabel(tk.Label(self.root, text="IP Address", font=self.header_font), None),
                GUILabel(tk.Label(self.root, text="State", font=self.header_font), None)
            ])

        logging.debug("Checking initial server states...")
        # Webservers
        for ws in self.config.webserver:
            # Role
            ws_role_label = GUILabel(
                tk.Label(self.root, text=ws.role), ws
            )

            # url
            ws_url_label = GUILabel(
                tk.Label(self.root, text=ws.url), ws
            )

            # IP address
            ws_ip_label = GUILabel(
                tk.Label(self.root, text=ws.ip_address), ws
            )

            # state
            ws_state_indicator = GUIStateIndicator(
                    tk.Label(self.root, text="up" if Pinger.ping_target(ws.url) else "down"),
                    ws
                )

            self.matrix_grid.append([
                ws_role_label,
                ws_url_label,
                ws_ip_label,
                ws_state_indicator
            ])
            self.indicators.append(ws_state_indicator)

        logging.debug("Root window opened.")

    def display_matrix(self):
        for dim in self.matrix_grid:
            for gui_element in dim:
                gui_element.element.config(
                    borderwidth=1,
                    relief="solid",
                    highlightbackground="grey",  # Set the border color to black
                    highlightthickness=1,  # Thickness of the highlight border
                    padx=10,
                    pady=5
                )
                gui_element.place_element(self.x, self.y)
                self.x += 1
            self.x = 0
            self.y += 1
