import django
django.setup()
from  __future__ import absolute_import,unicode_literals
from config import celery_app
from celery import shared_task

from django.contrib.auth import get_user_model




User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()

@celery_app.task()
def add(x, y):
    return x + y
