from __future__ import absolute_import, unicode_literals
# import django
# django.setup()
from celery import shared_task
from celery.utils.log import get_task_logger
from config import celery_app

from django.contrib.auth import get_user_model


User = get_user_model()
logger = get_task_logger(__name__)


@celery_app.task(track_started=True)
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@shared_task(name='users.tasks.add')
def add(x, y):
    # logger.info(self.request.id)
    logger.info('Adding {0} + {1}'.format(x, y))
    result = x + y
    return result
