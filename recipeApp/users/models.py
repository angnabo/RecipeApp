from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

from recipeApp.files.models import ImageFile


class Author(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING)
    full_name = models.CharField(max_length=250, validators=[MinLengthValidator(1)])
    profile_info = models.TextField(validators=[MinLengthValidator(1)])
    profile_picture = models.ForeignKey(ImageFile, on_delete=models.DO_NOTHING, null=True)
    created_date = models.DateTimeField('created_date')