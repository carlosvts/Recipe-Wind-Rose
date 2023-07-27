import os

import discord
import dotenv
import requests
from discord.errors import DiscordException

dotenv.load_dotenv()

# Discord Bot Connection


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in {self.user}")

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


# Giving bot permissions
intents = discord.Intents()
intents.messages = True
intents.message_content = True

client = MyClient(intents=intents)
if os.getenv('DISCORD-BOT-TOKEN') is not None:
    client.run(os.environ['DISCORD-BOT-TOKEN'])
else:
    raise DiscordException("Invalid Token")
