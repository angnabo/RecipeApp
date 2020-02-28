from django.forms import ModelForm
from recipeApp.recipes.models import Recipe, Comment


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'content']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
