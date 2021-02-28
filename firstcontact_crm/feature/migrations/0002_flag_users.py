# Generated by Django 3.0.12 on 2021-02-27 09:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feature', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='Activate this flag for these users.', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
    ]
