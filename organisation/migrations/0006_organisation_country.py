# Generated by Django 3.2.4 on 2021-06-20 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
        ('organisation', '0005_auto_20210309_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='country.country'),
        ),
    ]
