import os

import dotenv
import interactions
from interactions import OptionType, SlashContext, slash_command, slash_option

from api import DataFetcher, RecipeAPI

dotenv.load_dotenv()

# Creating recipeAPI
recipe_api = RecipeAPI()

# Creating Client
bot = interactions.Client()

# listen is like event from discord.py


@interactions.listen()
async def on_startup():
    print("Bot is ready!")


@slash_command(name="sim", description="por favor agora tem que ir")
async def por_favor(ctx: SlashContext):
    await ctx.send(f"Hi, {ctx.author.mention}")


@slash_command(
    name="recipe-by-ingredient", description="Get delicious recipes "
    "based on ingredients in your fridge!")
@slash_option(
    name="ingredients",
    description="Type comma-separated ingredients here!",
    required=True,
    opt_type=OptionType.STRING
)
async def fetch_recipe_and_process_data(ctx: SlashContext, ingredients: str):
    recipe_result = await recipe_api.get_recipes_by_ingredients(ingredients)
    _data_fetcher = DataFetcher(recipe_result)

    # Extracting results from DataFetcher
    recipe_name, recipe_image = _data_fetcher.extract_recipe_name_and_image(
        recipe_result)

    ingredients_have = _data_fetcher.extract_used_ingredients(
        recipe_result)

    missed_ingredients = _data_fetcher.extract_missed_ingredients(
        recipe_result)

    unused_ingredients = _data_fetcher.extract_unused_ingredients(
        recipe_result)


    ctx.send(embed=)

# Run the bot
bot.start(token=os.getenv('DISCORD-BOT-TOKEN'))
