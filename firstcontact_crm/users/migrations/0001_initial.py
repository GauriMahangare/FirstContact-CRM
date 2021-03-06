# Generated by Django 3.0.12 on 2021-02-27 09:51

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('organisation', '0002_auto_20210227_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Name of the user')),
                ('title', models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Miss.', 'Miss.'), ('Ms.', 'Ms.'), ('NotProvided', 'Prefer not to say')], default='NotProvided', max_length=25, verbose_name='Title')),
                ('first_name', models.CharField(blank=True, max_length=60, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=60, verbose_name='Last Name')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name='Phone number')),
                ('mobile_number', models.CharField(max_length=20, verbose_name='Mobile number')),
                ('is_admin', models.BooleanField(default=True)),
                ('is_team_manager', models.BooleanField(default=False)),
                ('is_team_member', models.BooleanField(default=False)),
                ('is_organisation_default', models.BooleanField(default=True)),
                ('is_profile_complete', models.BooleanField(default=False)),
                ('stripe_customer_id', models.CharField(blank=True, default='', max_length=50, verbose_name='Stripe customer id')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('userorganization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organisation.Organisation', verbose_name='User Work Organisation')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
