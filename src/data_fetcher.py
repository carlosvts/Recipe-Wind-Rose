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

    def format_ingredients(self, ingredients):
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
