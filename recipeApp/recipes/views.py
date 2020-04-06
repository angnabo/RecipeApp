from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from recipeApp.settings import *
from recipeApp.recipes.factories import RecipeFactory, CommentFactory, LikeFactory
from recipeApp.recipes.forms import RecipeForm, CommentForm
from recipeApp.utils import email_sender
from .models import Recipe, Like

ORDER_BY_HEADERS = ('name', 'content', 'username', 'date')


@login_required(login_url='users:login')
def index(request):
    return search(request)


@login_required(login_url='users:login')
def search(request):
    query = request.GET.get('query')
    if not query or not query.strip():  # query is empty or whitespace
        recipe_list = Recipe.objects.all().order_by('-created_date')
        paginated_recipes = get_recipes(request, recipe_list)
        url = reverse('recipes:search')
        context = {'recipe_list': paginated_recipes, 'title': 'Recipes', 'search_url': url}
        return render(request, 'recipes/index.html', context)
    else:
        recipe_list = Recipe.objects.filter(name__icontains=query, content__icontains=query).order_by('-created_date')
        paginated_recipes = get_recipes(request, recipe_list)
        url = reverse('recipes:search')
        context = {'recipe_list': paginated_recipes, 'search_query': query, 'title': 'Recipes', 'search_url': url}
        return render(request, 'recipes/index.html', context)


@login_required(login_url='users:login')
def get(request):
    query = request.GET.get('query')
    user_id = request.user.id
    if not query or not query.strip():  # query is empty or whitespace
        recipe_list = Recipe.objects.filter(user_id=user_id).order_by('-created_date')
        paginated_recipes = get_recipes(request, recipe_list)
        url = reverse('recipes:get')
        context = {'recipe_list': paginated_recipes, 'title': 'Your recipes', 'search_url': url}
        return render(request, 'recipes/index.html', context)
    else:
        recipe_list = Recipe.objects.filter(name__icontains=query, content__icontains=query, user_id=user_id).order_by(
            '-created_date')
        paginated_recipes = get_recipes(request, recipe_list)
        url = reverse('recipes:get')
        context = {'recipe_list': paginated_recipes, 'search_query': query, 'title': 'Your recipes', 'search_url': url}
        return render(request, 'recipes/index.html', context)


@login_required(login_url='users:login')
def activity(request):
    return render(request, 'recipes/activity.html')

@login_required(login_url='users:login')
def get_recipe_likes_activity(request):
    user = get_object_or_404(User, pk=request.user.id)
    date = datetime.now()+timedelta(days=-7)
    likes = list(Like.objects.filter(recipe__user_id=user.id, created_date__gt=date).order_by('created_date'))
    json_data = dict()
    for l in likes:
        try:
            likes_on_date = json_data.get(l.created_date.strftime("%m/%d/%Y"))
            if likes_on_date is None:
                json_data[l.created_date.strftime("%m/%d/%Y")] = 1
            else:
                json_data[l.created_date.strftime("%m/%d/%Y")] = likes_on_date+1
        except Exception as e:
            print(e)
    return JsonResponse(json_data, safe=False)


@login_required(login_url='users:login')
def add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(User, pk=request.user.id)
            recipe = form.save(commit=False)
            recipe.user = user
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
        form = RecipeForm(request.POST,  request.FILES, instance=recipe)
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
    user = get_object_or_404(User, pk=request.user.id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    new_like = LikeFactory.create(recipe, user)
    new_like.save()
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
