# Generated by Django 3.1.12 on 2021-06-28 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0004_alter_country_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
