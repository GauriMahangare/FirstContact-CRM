# Generated by Django 3.1.12 on 2021-06-28 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0002_alter_language_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
