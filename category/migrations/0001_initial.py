# Generated by Django 3.2.4 on 2021-06-21 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation', '0010_organisation_industry'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=200, verbose_name='status')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('dateTimeModified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('dateTimeCreated', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.organisation')),
            ],
            options={
                'verbose_name': 'Lead Category',
                'verbose_name_plural': 'Lead Category',
            },
        ),
    ]
