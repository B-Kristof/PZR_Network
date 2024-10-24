import argparse
import datetime
import logging
import discord
import sys


class DiscordBot:
    def __init__(self, token: str, user_id: int):
        self.token = token
        self.user_id = user_id
        intents = discord.Intents.default()
        intents.messages = True
        self.client = discord.Client(intents=intents)
        self.webserver = None

        @self.client.event
        async def on_ready():
            logging.debug(f'Logged in as {self.client.user}')
            await self.notify_user(self.webserver)
            await self.client.close()  # Close the client after sending the message

    async def notify_user(self, webserver):
        user = await self.client.fetch_user(self.user_id)  # Await the fetch_user call
        if user:  # Ensure user is fetched
            try:
                await user.send(f"{webserver.role} ({webserver.url}) Server down!")  # Await the send call
                logging.info("Message sent, logging out...")
            except Exception as e:
                logging.error(f"Failed to send message: {e}")

    async def notify_user_startup(self, webserver):
        user = await self.client.fetch_user(self.user_id)  # Await the fetch_user call
        if user:  # Ensure user is fetched
            try:
                await user.send(f"Monitor setup complete for {webserver.role} ({webserver.url})")
                logging.info("Startup message sent, logging out...")
                await self.client.close()  # Close the client after sending the message
            except Exception as e:
                logging.error(f"Failed to send startup message: {e}")

    def start(self):
        # Use run() to start the bot
        self.client.run(self.token)

    def interface(self, command, webserver):
        if command == "start":
            self.start()
        elif command == "notify_user":
            self.webserver = webserver
            self.start()

class Webserver:
    def __init__(self, role: str, url: str):
        self.role = role
        self.url = url

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Discord bot to notify users about webserver status.")
    parser.add_argument('--token', type=str, required=True, help="Discord bot token")
    parser.add_argument('--user-id', type=int, required=True, help="Discord user ID to notify")
    parser.add_argument('--command', type=str, required=True, choices=['start', 'notify_user'], help="Command to execute")
    parser.add_argument('--role', type=str, help="Webserver role")
    parser.add_argument('--url', type=str, help="Webserver URL")

    args = parser.parse_args()

    # Create a Webserver object if role and url are provided
    webserver = None
    if args.role and args.url:
        webserver = Webserver(args.role, args.url)

    # Create the bot and execute the command
    bot = DiscordBot(token=args.token, user_id=args.user_id)
    bot.interface(args.command, webserver)


if __name__ == '__main__':
    main()
