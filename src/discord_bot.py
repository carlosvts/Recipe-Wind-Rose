import os

import discord
import dotenv
import requests
from discord.errors import DiscordException
from discord.ext import commands
from discord.ext.commands import Command

dotenv.load_dotenv()

# Discord Bot Connection

# Giving bot permissions
intents = discord.Intents()
intents.messages = True
intents.message_content = True
intents.typing = True
intents.emojis_and_stickers = True

# Creating Client
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"Logged in {client.user.name}")  # type: ignore


@client.command()
async def teste(ctx):
    await ctx.channel.send("Testado")

if os.getenv('DISCORD-BOT-TOKEN') is not None:
    client.run(os.environ['DISCORD-BOT-TOKEN'])
else:
    raise DiscordException("Invalid Token")
