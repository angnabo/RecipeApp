# Generated by Django 2.2.8 on 2020-02-10 10:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_auto_20200210_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=250, validators=[django.core.validators.MinLengthValidator(1)])),
                ('profile_info', models.TextField(validators=[django.core.validators.MinLengthValidator(1)])),
                ('created_date', models.DateTimeField(verbose_name='created_date')),
                ('profile_picture', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='recipes.ImageFile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]