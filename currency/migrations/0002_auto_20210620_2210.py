# Generated by Django 3.2.4 on 2021-06-20 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(blank=True, max_length=1, verbose_name='Symbol'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='thousand_seperator',
            field=models.CharField(blank=True, max_length=1, verbose_name='thousand_seperator'),
        ),
    ]
