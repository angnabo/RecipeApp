from datetime import datetime

from recipeApp.recipes.models import Like


class RecipeFactory:

    @staticmethod
    def create(form, user):
        form.full_clean()
        recipe = form.save(commit=False)
        recipe.created_date = datetime.now()
        recipe.user = user
        return recipe


class CommentFactory:

    @staticmethod
    def create(form, recipe, user):
        form.full_clean()
        comment = form.save(commit=False)
        comment.recipe = recipe
        comment.likes = 0
        comment.created_date = datetime.now()
        comment.user = user
        return comment


class LikeFactory:

    @staticmethod
    def create(recipe, user):
        like = Like()
        like.recipe = recipe
        like.created_date = datetime.now()
        like.user = user
        return like
