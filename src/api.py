import asyncio
import os

import dotenv
import requests

from fetchers import DataFetcher, RecipeFetcher

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
        # print("RECIPE INSIDE GETRECIPE METHOD", recipe)

        _headers = {
            'x-api-key': API_KEY,
        }

        _params = {
            'query': recipe,
            "number": "1",
        }
        self.API_ENDPOINT = BASE_RECIPES_URL + "complexSearch"
        if diet is not None:
            _params['diet'] = diet
        if cuisine is not None:
            _params['cuisine'] = cuisine

        # print("API ENDPOINT", self.API_ENDPOINT)
        response = requests.get(
            self.API_ENDPOINT, headers=_headers, params=_params)
        # print(response.request)
        # print("STATUSCODE: ", response.status_code)
        # print(response.json())
        recipe_info = response.json()
        return recipe_info

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


# TEST
# if __name__ == '__main__':
#     async def test():
#         """
#             Just a test to see if i catch correctly the info from the API
#         """
#         recipe = RecipeAPI()

#         recipeTest = await recipe.get_recipe("pasta", "italian", "vegan")

#         fetcher = RecipeFetcher(recipeTest)
#         fetcher.fetch_info()
#         print("\n")

#         return recipeTest
#         ...

#     asyncio.run(test())
