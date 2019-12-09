from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from recipes.forms import RecipeForm
from .models import Recipe


def index(request):
    recipe_list = Recipe.objects.all()  # .order_by('-created_date')
    paginator = Paginator(recipe_list, 5)
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    context = {'recipe_list': recipes}
    return render(request, 'recipes/index.html', context)


def add(request):
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
