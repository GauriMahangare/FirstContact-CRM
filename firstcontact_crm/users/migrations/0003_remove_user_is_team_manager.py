# Generated by Django 3.0.12 on 2021-03-07 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210228_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_team_manager',
        ),
    ]
