from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=250, validators=[MinLengthValidator(1)])
    content = models.TextField(blank=False, validators=[MinLengthValidator(1)])
    created_date = models.DateTimeField('created_date')
    likes = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

