from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

from recipeApp.files.models import ImageFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    profile_info = models.TextField(validators=[MinLengthValidator(1)], null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default-profile.png')
    created_date = models.DateTimeField('created_date')
