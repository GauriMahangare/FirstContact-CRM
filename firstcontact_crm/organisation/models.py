from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.auth import get_user, get_user_model
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.
User = settings.AUTH_USER_MODEL

class Organisation(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    work_org_name = models.CharField('Work organisation',
        max_length=300,
        blank=True,
        help_text='Required: Organisation Name'
    )
    work_address_line1 = models.CharField(
        'Address Line 1',
        max_length=60,
        default='',
        help_text='Required: First Line of address'
    )
    work_address_line2 = models.CharField(
        'Address Line 2',
        max_length=60,
        blank=True,
    )
    work_address_line3 = models.CharField(
        'Address Line 3',
        max_length=60,
        blank=True,
    )
    work_address_line4 = models.CharField(
        'Address Line 4',
        max_length=60,
        blank=True,
    )
    work_address_postcode = models.CharField(
        'Postcode',
        max_length=30,
        default='',
        help_text='Required: Postcode'
    )
    is_verified = models.BooleanField(default=True)
    is_access_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )

    subscriptionType = models.TextField('Subscription',
        blank=True,
    )

    def __str__(self):
        return f"{self.work_org_name}"

    def get_absolute_url(self):
        return reverse('organisation-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'

def get_queryset(self):
        return User.objects.filter(user=1)

# Code has been commented as current request user cannot be accessed in models.

# def post_organisation_created_signal(sender, instance, created, **kwargs):
#     if created:
#         print("organisation created")
#         # print(Organisation)
#         # print(instance.user)
#         # user = instance.request.user
#         # User = settings.AUTH_USER_MODEL
#         print(instance)
#         print(instance.created_by)
#         queryset = users.User.objects.filter(user=instance.created_by)

#         # queryset = User.objects.filter(pk=instance.created_by)
#         # user = get_queryset(instance.created_by)
#         print(queryset)
#         # user = instance.User
#         # user.is_organisation_default = False
#         # user.userorganization = sender.Organisation.id
#         # user.objects.save()
#     print("organisation not created")


# post_save.connect(post_organisation_created_signal, sender=Organisation,)