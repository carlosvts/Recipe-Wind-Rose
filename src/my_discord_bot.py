import os
from typing import Optional

import dotenv
import interactions
from interactions import OptionType, SlashContext, slash_command, slash_option

from api import RecipeAPI
from fetchers import DataFetcher, RecipeFetcher

dotenv.load_dotenv()

# Creating recipeAPI
recipe_api = RecipeAPI()

# Creating Client
bot = interactions.Client()


@interactions.listen()
async def on_startup():
    print("Bot is ready!")


# ------------------------- RECIPE BY INGREDIENT COMMAND ---------------------
@slash_command(
    name="recipe-by-ingredient", description=(
        "Get delicious recipes based on ingredients in your fridge!"))
@slash_option(
    name="ingredients",
    description="Type comma-separated ingredients here!",
    required=True,
    opt_type=OptionType.STRING
)
async def fetch_recipe_and_process_data(ctx: SlashContext, ingredients: str):
    recipe_response = await recipe_api.get_recipes_by_ingredients(ingredients)
    _data_fetcher = DataFetcher(recipe_response)

    # Extracting results from DataFetcher
    recipe_name, recipe_url = _data_fetcher.extract_recipe_name_and_image(
        recipe_response
    )

    ingredients_have = _data_fetcher.extract_used_ingredients(
        recipe_response
    )

    missed_ingredients = _data_fetcher.extract_missed_ingredients(
        recipe_response
    )

    unused_ingredients = _data_fetcher.extract_unused_ingredients(
        recipe_response
    )

    recipe_final_result = _data_fetcher.format_response_to_user(
        recipe_name, ingredients_have, missed_ingredients, unused_ingredients
    )

    recipe_img = interactions.Embed(
        "Delicious!",  # type: ignore
        images=interactions.EmbedAttachment(recipe_url)  # type: ignore
    )

    await ctx.send(embed=recipe_img)
    await ctx.send(content=recipe_final_result)

# --------------------- SEARCH RECIPE COMMAND -------------------------------


@slash_command(name="search-recipe", description=(
    "Search some delicious recipes, they will flow like wind")
)
@slash_option(
    name="recipe",
    description="Type some recipe (Example: pasta)",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="cuisine",
    description="should add some specific cuisine? you can!(Example: italian)",
    required=False,
    opt_type=OptionType.STRING

)
@slash_option(
    name="diet",
    description="Want to add a diet? So here we go (Example: vegetarian)",
    required=False,
    opt_type=OptionType.STRING,

)
async def search_recipe_query(
    ctx: SlashContext, recipe: str, cuisine: Optional[str] = None,
    diet: Optional[str] = None
):
    _recipe_response = await recipe_api.get_recipe(recipe, cuisine, diet)
    _data_fetcher = RecipeFetcher(_recipe_response)
    recipe_name, recipe_url = _data_fetcher.fetch_info()

    recipe_image = interactions.Embed(
        title="Delicious!", url=recipe_url,
        images=interactions.EmbedAttachment(recipe_url)  # type: ignore
    )

    await ctx.send(embed=recipe_image)
    await ctx.send(content=_data_fetcher.format_response_to_user(recipe_name))

    # TODO Diet has some specific things to do, check docs later

# Run the bot
bot.start(token=os.getenv('DISCORD-BOT-TOKEN'))
