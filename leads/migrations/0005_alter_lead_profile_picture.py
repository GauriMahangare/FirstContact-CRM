# Generated by Django 3.2 on 2021-05-31 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_alter_lead_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='Leads/profile_pictures/'),
        ),
    ]
