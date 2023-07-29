import asyncio
import os

import dotenv
import requests

dotenv.load_dotenv()

# Spoonacular API
# Defining base URL'S
# REMINDER: the Spoonacular url is case sensitive (camelCase)
BASE_RECIPES_URL = "https://api.spoonacular.com/recipes/"
BASE_INGREDIENTS_URL = "https://api.spoonacular.com/food/ingredients/search"
API_KEY = "?apiKey=" + os.environ['SPOONACULAR-API-KEY'] + "&"


class RecipeAPI():
    API_ENDPOINT = ""

    def __init__(self, api_key=API_KEY) -> None:
        self.api_key = API_KEY

    async def get_recipes_by_ingredients(self, ingredients: str):
        """
        Uses request library to connect with Spoonacular API and find
        good recipes based on user-typed ingredients
        Then, it will respond one recipe, maybe i will expand this in the
        future
        """
        # Treating user input to be like this:
        # ingredients=apples,+flour,+sugar
        ingredients = ingredients.strip()
        ingredients = ingredients.replace(" ", "")
        ingredients = ingredients.replace(",", ",+")

        self.API_ENDPOINT = (BASE_RECIPES_URL + "findByIngredients"
                             + API_KEY + f"ingredients={ingredients}"
                             + "&number=1")

        print("API ENDPOINT", self.API_ENDPOINT)
        response = requests.get(self.API_ENDPOINT)
        _recipe_info = response.json()
        print(_recipe_info)
        return _recipe_info


class DataFetcher():
    def __init__(self, data) -> None:
        self.data = data

    def extract_recipe_name_and_image(self, data):
        recipe_name = data[0]["title"]
        recipe_image = data[0]["image"]
        return recipe_name, recipe_image

    def extract_used_ingredients(self, data):
        ingredients_user_have = {}
        for ingredient in data[0]["usedIngredients"]:
            name = ingredient["name"]
            amount = ingredient["original"]
            ingredients_user_have[name] = amount
        return ingredients_user_have

    def extract_missed_ingredients(self, data):
        missed_ingredients = {}
        for ingredient in data[0]["missedIngredients"]:
            name = ingredient["name"]
            amount = ingredient["original"]
            missed_ingredients[name] = amount
        return missed_ingredients

    def extract_unused_ingredients(self, data):
        unused_ingredients = [ingredient["name"]
                              for ingredient in data[0]["unusedIngredients"]]
        return unused_ingredients

    def print_recipe_info(self, recipe_name, recipe_image,
                          ingredients_user_have, missed_ingredients,
                          unused_ingredients):
        print("Recipe Name:", recipe_name)
        print("Recipe Image URL:", recipe_image)

        print("\nIngredients you have:")
        for ingredient, amount in ingredients_user_have.items():
            print("-", ingredient, ":", amount)

        print("\nIngredients you don't have:")
        for ingredient, amount in missed_ingredients.items():
            print("-", ingredient, ":", amount)


async def test():
    """
        Just a test to see if i catch correctly the info from the API
    """
    recipe = RecipeAPI()

    recipe_info = await recipe.get_recipes_by_ingredients(
        "apples, flour, sugar")

    data_fetcher = DataFetcher(recipe_info)

    recipe_name, recipe_image = data_fetcher.extract_recipe_name_and_image(
        recipe_info)
    ingredients_have = data_fetcher.extract_used_ingredients(recipe_info)
    missed_ingredients = data_fetcher.extract_missed_ingredients(recipe_info)
    unused_ingredients = data_fetcher.extract_unused_ingredients(recipe_info)

    data_fetcher.print_recipe_info(
        recipe_name, recipe_image, ingredients_have,
        missed_ingredients, unused_ingredients
    )


asyncio.run(test())
