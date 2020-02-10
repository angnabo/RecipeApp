from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

from recipeApp.users.models import Author


class Recipe(models.Model):
    name = models.CharField(max_length=250, validators=[MinLengthValidator(1)])
    content = models.TextField(blank=False, validators=[MinLengthValidator(1)])
    created_date = models.DateTimeField('created_date')
    likes = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


