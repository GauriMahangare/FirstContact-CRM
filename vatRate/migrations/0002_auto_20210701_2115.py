# Generated by Django 3.1.12 on 2021-07-01 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vatRate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vatrate',
            name='description',
            field=models.CharField(blank=True, max_length=100, verbose_name='Description'),
        ),
    ]
