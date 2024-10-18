import logging
import discord
from Models import Webserver
import asyncio


class DiscordNotifier:
    def __init__(self, token: str, user_id: int, webserver: Webserver):
        self.token = token
        self.user_id = user_id
        self.webserver = webserver
        intents = discord.Intents.default()
        intents.messages = True
        self.client = discord.Client(intents=intents)

        # Register the event handlers
        self.client.event(self.on_ready)  # This must remain async

    async def notify_user(self):
        user = await self.client.fetch_user(self.user_id)  # Await the fetch_user call
        if user:  # Ensure user is fetched
            await user.send(f"{self.webserver.role} ({self.webserver.url}) Server down!")  # Await the send call

    async def notify_user_startup(self):
        user = await self.client.fetch_user(self.user_id)  # Await the fetch_user call
        if user:  # Ensure user is fetched
            await user.send(f"Monitor setup complete for {self.webserver.role} ({self.webserver.url})")

    async def on_ready(self):
        logging.debug(f'Logged in as {self.client.user}')
        await self.notify_user_startup()

    def start(self):
        # Use run() to start the bot
        self.client.run(self.token)


def discord_notifier_interface(command, bot: DiscordNotifier):
    if command == "start":
        bot.start()
    elif command == "notify_user":
        asyncio.run(bot.notify_user())
