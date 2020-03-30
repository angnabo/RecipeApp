from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

from recipeApp.users.models import Profile


class Recipe(models.Model):
    name = models.CharField(max_length=250, validators=[MinLengthValidator(1)])
    content = models.TextField(blank=False, validators=[MinLengthValidator(1)])
    created_date = models.DateTimeField('created_date')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField(blank=False, validators=[MinLengthValidator(1)])
    created_date = models.DateTimeField('created_date')
    likes = models.IntegerField()


class Like(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='likes', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_date = models.DateField('created_date')


