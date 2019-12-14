from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm


class Recipe(models.Model):
    name = models.CharField(max_length=250)
    content = models.TextField()
    created_date = models.DateTimeField('created_date')
    likes = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

