# Generated by Django 3.2.4 on 2021-06-20 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0005_auto_20210309_1956'),
        ('leads', '0014_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='organisation',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, to='organisation.organisation'),
            preserve_default=False,
        ),
    ]
