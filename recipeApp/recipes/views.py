from datetime import datetime, timezone

from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from recipeApp.recipes.forms import RecipeForm
from .models import Recipe


def index(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    else:
        recipe_list = Recipe.objects.all().order_by('-created_date')
        paginator = Paginator(recipe_list, 5)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        context = {'recipe_list': recipes}
        return render(request, 'recipes/index.html', context)


def search(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    else:
        query = request.GET.get('query')
        recipe_list = Recipe.objects.filter(name__icontains=query, content__icontains=query).order_by('-created_date')
        paginator = Paginator(recipe_list, 5)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        context = {'recipe_list': recipes}
        return render(request, 'recipes/index.html', context)


def add(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    else:
        if request.method == 'POST':
            form = RecipeForm(request.POST)
            if form.is_valid():
                form.full_clean()
                recipe = form.save(commit=False)
                recipe.created_date = datetime.now(timezone.utc)
                recipe.likes = 0
                user = request.user
                recipe.user = user
                recipe.save()
                return redirect('recipes:details', recipe_id=recipe.id)
            else:
                return render(request, 'recipes/add_recipe.html', {'form': form, 'title': 'Add Recipe'})
        else:
            form = RecipeForm()
            return render(request, 'recipes/add_recipe.html', {'form': form, 'title': 'Add Recipe'})


def edit(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('users:login')
    else:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            form = RecipeForm(request.POST, instance=recipe)
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.save()
                return redirect('recipes:details', recipe_id=recipe_id)
        else:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            form = RecipeForm(request.POST or None, instance=recipe)
            return render(request, 'recipes/add_recipe.html', {'form': form, 'title': 'Edit Recipe'})


def delete(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('users:login')
    else:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.delete()
        return redirect('recipes:index')


def details(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('users:login')
    else:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return render(request, 'recipes/recipe_details.html', {'recipe': recipe})


def like(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('users:login')
    else:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.likes += 1
        recipe.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def dislike(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('users:login')
    else:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.likes -= 1
        recipe.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
