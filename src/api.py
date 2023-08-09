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
API_KEY = os.environ['SPOONACULAR-API-KEY']
BY_URL_API_KEY = "?apiKey=" + API_KEY + "&"


class RecipeAPI():
    API_ENDPOINT = ""

    def __init__(self, api_key=BY_URL_API_KEY) -> None:
        self.api_key = BY_URL_API_KEY

    async def get_recipe(self,
                         recipe: str,
                         cuisine: str | None = None, diet: str | None = None
                         ):
        """
        Get a recipe based on 3 params
        recipe -> natural human language recipe like Pasta
        cuisine -> Optional, if user wants some specific cuisine like italian
        pasta
        diet -> Optional, if user wants some specific diet like vegetarian  
        """
        # Just slicing some typos
        recipe = recipe.strip()
        recipe = recipe.replace(" ", "")

        _headers = {
            'x-api-key': API_KEY,
        }
        # Assuming that user only want recipe based on query
        self.API_ENDPOINT = BASE_RECIPES_URL + "complexSearch"
        if diet is not None:
            _headers['diet'] = diet
        if cuisine is not None:
            _headers['cuisine'] = cuisine

        print("API ENDPOINT", self.API_ENDPOINT)
        response = requests.get(self.API_ENDPOINT, headers=_headers)
        print("STATUSCODE: ", response.status_code)
        print(response.json())

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
                             + BY_URL_API_KEY + f"ingredients={ingredients}"
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

        recipeTest = await recipe.get_recipe("pasta", "italian", "vegan")
        return recipeTest
        ...

    asyncio.run(test())
