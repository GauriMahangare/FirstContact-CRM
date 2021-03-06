# Generated by Django 3.2.4 on 2021-06-20 23:26

from django.db import migrations, models
import django.db.models.deletion
import firstcontact_crm.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0002_alter_language_created_by'),
        ('country', '0004_alter_country_created_by'),
        ('users', '0003_remove_user_is_team_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='country.country'),
        ),
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='language.language'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=firstcontact_crm.users.models.user_profile_image_directory_path),
        ),
    ]
