from datetime import datetime


class RecipeFactory:

    @staticmethod
    def create(form, author):
        form.full_clean()
        recipe = form.save(commit=False)
        recipe.created_date = datetime.now()
        recipe.likes = 0
        recipe.author = author
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
