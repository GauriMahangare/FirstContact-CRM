# Generated by Django 3.2.4 on 2021-06-20 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0003_country_language'),
        ('language', '0001_initial'),
        ('organisation', '0007_remove_organisation_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='country.country'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='language.language'),
        ),
    ]
