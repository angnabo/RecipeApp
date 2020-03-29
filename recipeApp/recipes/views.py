from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string

from recipeApp.settings import *
from recipeApp.recipes.factories import RecipeFactory, CommentFactory
from recipeApp.recipes.forms import RecipeForm, CommentForm
from recipeApp.utils import email_sender
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
            user = get_object_or_404(User, pk=request.user.id)
            recipe = RecipeFactory.create(form, user)
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
    items_per_page = 10
    paginator = Paginator(recipe_list, items_per_page)
    page = request.GET.get('page')
    return paginator.get_page(page)


@login_required(login_url='users:login')
def add_comment(request, recipe_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        comment = CommentFactory.create(form, recipe, user)
        comment.save()

        # send email
        recipe_user_email = get_object_or_404(User, pk=recipe.user_id).email
        subject = 'You received a comment on your recipe!'
        try:
            template = render_to_string("emails/comment_notification_email.html",
                                        {'comment': comment, 'username': user.get_full_name()})
            email_sender.send_email([recipe_user_email], subject, template)
        except Exception as e:
            print(e)
        return redirect('recipes:details', recipe_id=recipe_id)
    else:
        return redirect('recipes:details', recipe_id=recipe_id)

