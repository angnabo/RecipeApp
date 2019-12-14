from datetime import datetime, timezone

from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from recipeApp.recipes.forms import RecipeForm
from .models import Recipe


def index(request):
    recipe_list = Recipe.objects.all()  # .order_by('-created_date')
    paginator = Paginator(recipe_list, 5)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    context = {'recipe_list': recipes}
    return render(request, 'recipes/index.html', context)


def add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_date = datetime.now(timezone.utc)
            recipe.likes = 0
            user = request.user
            recipe.save()
            return HttpResponseRedirect('/recipes')
    else:

        form = RecipeForm()
        return render(request, 'recipes/recipe_form.html', {'form': form})


def details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/detail.html', {'recipe': recipe})


def like(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.likes += 1
    recipe.save()
    return HttpResponseRedirect(reverse('recipes:details', args=(recipe.id,)))
