class DataFetcher():
    def __init__(self, data) -> None:
        self.data = data

    def extract_recipe_name_and_image(self, data):
        """
        Fetch recipe name and image from the api response
        """
        recipe_name = data[0]["title"]
        recipe_image = data[0]["image"]
        return recipe_name, recipe_image

    def extract_used_ingredients(self, data):
        """
        Extract from the JSON api response the ingredients that will use for
        the recipe
        """
        ingredients_user_have = {}
        for ingredient in data[0]["usedIngredients"]:
            name = ingredient["name"]
            amount = ingredient["original"]
            ingredients_user_have[name] = amount
        return ingredients_user_have

    def extract_missed_ingredients(self, data):
        """
        Extract from the JSON api response the ingredients that are missing
        for the recipe
        """
        missed_ingredients = {}
        for ingredient in data[0]["missedIngredients"]:
            name = ingredient["name"]
            amount = ingredient["original"]
            missed_ingredients[name] = amount
        return missed_ingredients

    def extract_unused_ingredients(self, data):
        """
        Extract from the JSON api response the ingredients that user has
        passed but he will not use for this recipe
        """
        unused_ingredients = [ingredient["name"]
                              for ingredient in data[0]["unusedIngredients"]]
        return unused_ingredients

    def format_ingredients(self, ingredients):
        """
        Iterating trough all lists to get a formated string
        """
        formatted = ""
        for ingredient, amount in ingredients.items():
            formatted += f"- {ingredient}: {amount}\n"
        return formatted

    def format_response_to_user(self, recipe_name,
                                ingredients_user_have, missed_ingredients,
                                unused_ingredients):

        output = f"""Recipe Name: {recipe_name}

            Ingredients you have:
            {self.format_ingredients(ingredients_user_have)}

            Ingredients you don't have:
            {self.format_ingredients(missed_ingredients)}

            """

        return output


class RecipeFetcher():
    """
    A similar DataFetcher, but used to fetch get_recipe method from RecipeApi
    """

    def __init__(self, data: dict) -> None:
        self.data = data

    def fetch_info(self):
        """
        Fetches info from JSON-like response from RecipeAPI
        """
        # Used for getting the first recipe from api_response
        FIRST_RECIPE_GETTER = self.data['results'][0]
        RECIPE_NAME = FIRST_RECIPE_GETTER['title']
        RECIPE_IMAGE = FIRST_RECIPE_GETTER['image']

        # TODO REMOVE THIS LATER, USED ONLY FOR DEBUGGING PORPOUSES
        print(f"FIRST_RECIPE_GETTER = {FIRST_RECIPE_GETTER}"
              f"RECIPENAME: {RECIPE_NAME}"
              f"RECIPEIMAGE: {RECIPE_IMAGE}")

        return RECIPE_NAME, RECIPE_IMAGE
