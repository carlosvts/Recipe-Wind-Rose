import os

import dotenv
import interactions
from interactions import SlashContext, slash_command

dotenv.load_dotenv()

# Creating Client
bot = interactions.Client()

# listen is like event from discord.py


@interactions.listen()
async def on_startup():
    print("Bot is ready!")


@slash_command(name="sim", description="por favor agora tem que ir")
async def por_favor(ctx: SlashContext):
    await ctx.send(f"Hi, {bot.user.mention}")


# Run the bot
bot.start(token=os.getenv('DISCORD-BOT-TOKEN'))
