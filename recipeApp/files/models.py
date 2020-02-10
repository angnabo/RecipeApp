from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


class ImageFile(models.Model):
    name = models.CharField(max_length=250, validators=[MinLengthValidator(1)])
    key_id = models.CharField(max_length=250)
    created_date = models.DateTimeField('created_date')
    created_by_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

