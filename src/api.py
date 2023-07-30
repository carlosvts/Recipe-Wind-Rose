import asyncio
import os

import dotenv
import requests

from data_fetcher import DataFetcher

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
        print(response.status_code)
        _recipe_info = response.json()
        return _recipe_info


if __name__ == '__main__':
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
        missed_ingredients = data_fetcher.extract_missed_ingredients(
            recipe_info)
        unused_ingredients = data_fetcher.extract_unused_ingredients(
            recipe_info)

        data_fetcher.format_response_to_user(
            recipe_name, ingredients_have,
            missed_ingredients, unused_ingredients
        )

    asyncio.run(test())
