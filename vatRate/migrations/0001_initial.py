# Generated by Django 3.1.12 on 2021-07-01 20:10

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
            name='VatRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='VAT Rate')),
                ('dateTimeModified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('dateTimeCreated', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation.organisation')),
            ],
            options={
                'verbose_name': 'VAT Rate',
                'verbose_name_plural': 'VAT Rates',
            },
        ),
    ]
