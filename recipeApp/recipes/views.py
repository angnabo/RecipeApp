from datetime import datetime, timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from recipeApp.recipes.factories import RecipeFactory
from recipeApp.recipes.forms import RecipeForm
from .models import Recipe

ORDER_BY_HEADERS = ('name', 'content', 'username', 'date')


@login_required(login_url='users:login')
def index(request):
    return search(request)


def search(request):
    query = request.GET.get('query')
    if not query or not query.strip():  # query is empty or whitespace
        recipe_list = Recipe.objects.all().order_by('-created_date')
        paginated_recipes = get_recipes(request, recipe_list)
        context = {'recipe_list': paginated_recipes}
        return render(request, 'recipes/index.html', context)
    else:
        recipe_list = Recipe.objects.filter(name__icontains=query, content__icontains=query).order_by('-created_date')
        paginated_recipes = get_recipes(request, recipe_list)
        context = {'recipe_list': paginated_recipes, 'search_query': query}
        return render(request, 'recipes/index.html', context)


@login_required(login_url='users:login')
def add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = RecipeFactory.create(form, request.user)
            recipe.save()
            return redirect('recipes:details', recipe_id=recipe.id)
        else:
            return render(request, 'recipes/add_recipe.html', {'form': form, 'title': 'Add Recipe'})
    else:
        form = RecipeForm()
        return render(request, 'recipes/add_recipe.html', {'form': form, 'title': 'Add Recipe'})


@login_required(login_url='users:login')
def edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.full_clean()
            form.save()
            return redirect('recipes:details', recipe_id=recipe_id)
        else:
            return render(request, 'recipes/add_recipe.html', {'form': form, 'title': 'Edit Recipe'})
    else:
        form = RecipeForm(request.POST or None, instance=recipe)
        return render(request, 'recipes/add_recipe.html', {'form': form, 'title': 'Edit Recipe'})


@login_required(login_url='users:login')
def delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('recipes:index')


@login_required(login_url='users:login')
def details(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_details.html', {'recipe': recipe})


@login_required(login_url='users:login')
def like(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.likes += 1
    recipe.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='users:login')
def dislike(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.likes -= 1
    recipe.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_recipes(request, recipe_list):
    items_per_page = 5
    paginator = Paginator(recipe_list, items_per_page)
    page = request.GET.get('page')
    return paginator.get_page(page)
