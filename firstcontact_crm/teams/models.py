from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth import get_user, get_user_model
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from organisation.models import Organisation
from invitations.utils import get_invitation_model
from invitations.models import Invitation

# Create your models here.
User = settings.AUTH_USER_MODEL

class Team(models.Model):
    created_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)

    name = models.CharField('Team Name',
        max_length=300,
        default='',
        help_text='Team Name'
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )
    description = models.TextField('Team Description',
        default='',
        blank=True,
        help_text='Enter Team objectives here'
    )
    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('team-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
# Create your models here.


