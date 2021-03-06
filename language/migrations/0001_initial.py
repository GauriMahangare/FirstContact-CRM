# Generated by Django 3.2.4 on 2021-06-20 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_name', models.CharField(max_length=400, verbose_name='ISO Language Name')),
                ('native_name', models.CharField(blank=True, max_length=400, verbose_name='Native name')),
                ('alphanumeric2_iso639_1_code', models.CharField(max_length=2, verbose_name='ISO639-1 ISO Language code')),
                ('alphanumeric3_iso639_2T_code', models.CharField(max_length=3, verbose_name='ISO639-2T ISO Language code')),
                ('alphanumeric3_iso639_2B_code', models.CharField(max_length=3, verbose_name='ISO639-2B ISO Language code')),
                ('alphanumeric3_iso639_3_code', models.CharField(blank=True, max_length=10, verbose_name='ISO639-3 ISO Language code')),
                ('description', models.TextField(blank=True)),
                ('isActive', models.BooleanField(default=True)),
                ('dateTimeModified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('dateTimeCreated', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Language',
            },
        ),
    ]
