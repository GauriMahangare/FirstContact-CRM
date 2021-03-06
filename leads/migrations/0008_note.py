# Generated by Django 3.2 on 2021-06-03 20:14

from django.db import migrations, models
import django.db.models.deletion
import leads.models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0007_alter_lead_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to=leads.models.lead_note_attachment_directory_path)),
                ('dateTimeModified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('dateTimeCreated', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followups', to='leads.lead')),
            ],
            options={
                'verbose_name': 'Notes',
                'verbose_name_plural': 'Notes',
            },
        ),
    ]
