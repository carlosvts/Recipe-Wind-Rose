import os

import discord
import dotenv
from discord import app_commands
from discord.errors import DiscordException
from discord.ext import commands
from discord.ext.commands import Context
from discord.interactions import Interaction

dotenv.load_dotenv()

# Discord Bot Connection

# Giving bot permissions
intents = discord.Intents()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.typing = True
intents.emojis_and_stickers = True

# Creating Client
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"Logged in {client.user.name}")  # type: ignore


@client.command()  # type: ignore
async def teste(ctx: Context):
    await ctx.channel.send("Testado")  # type: ignore

# Run the bot
if os.getenv('DISCORD-BOT-TOKEN') is not None:
    client.run(os.environ['DISCORD-BOT-TOKEN'])
else:
    raise DiscordException("Invalid Token")
