from django.forms import ModelForm
from recipeApp.recipes.models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'content']