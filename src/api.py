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

    def get_recipes_by_ingredients(self, ingredients: str):
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
        print(response.content)


recipe = RecipeAPI()
recipe.get_recipes_by_ingredients("apples,flour,suggar")
