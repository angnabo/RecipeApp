from datetime import datetime, timezone


class RecipeFactory:

    @staticmethod
    def create(form, author):
        form.full_clean()
        recipe = form.save(commit=False)
        recipe.created_date = datetime.now()
        recipe.likes = 0
        recipe.author = author
        return recipe
