from django.db import models
from datetime import date
import uuid
from django.db.models.fields import UUIDField
from django.db.models.query_utils import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from organisation.models import Organisation
from teams.models import Team
from django.urls import reverse
from django.template.loader import render_to_string

# Create your models here.

User = settings.AUTH_USER_MODEL
# class Campaign(models.Model):
#     user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)

#     description = models.CharField(
#         'Description',
#         max_length=200,
#     )
#     dateTimeModified = models.DateTimeField(
#         'Last Modified',
#         auto_now =True,
#     )

#     dateTimeCreated = models.DateTimeField(
#         'Created',
#         auto_now_add =True,
#     )

#     def __str__(self):
#         return "{self.description}".format(self=self)

#     class Meta:
#         verbose_name = 'Campaign'
#         verbose_name_plural = 'Campaigns'


class Category(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    status = models.CharField(
        'status',
        max_length=200,
        blank=True,
    )
    description = models.TextField(
        'Description',
        blank=True,
    )
    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now=True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )

    def __str__(self):
        return "{self.status}".format(self=self)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'


# class LeadManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset()

class Lead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='added_by')

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )

    team = models.ForeignKey(
        Team,
        null=True,
        on_delete=models.SET_NULL,
    )

    assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assinged_agent',
    )
    source = models.CharField('Source',
                              max_length=200,
                              )

    class TitleChoices(models.TextChoices):
        Mr = 'Mr.', _('Mr.')
        Mrs = 'Mrs.', _('Mrs.')
        Miss = 'Miss.', _('Miss.')
        Ms = 'Ms.', _('Ms.')
        default = '', _('Prefer not to say')
    title = models.CharField(
        'Title',
        max_length=25,
        choices=TitleChoices.choices,
        default=TitleChoices.default,
    )
    first_name = models.CharField('First Name',
                                  max_length=60,
                                  )
    last_name = models.CharField('Last Name',
                                 max_length=60,
                                 )
    date_of_birth = models.DateField('Date of Birth',
                                     blank=True,
                                     null=True,
                                     )
    age = models.IntegerField(
        'Age',
        default=0,
        blank=True,
    )
    work_org_name = models.CharField('Work organisation',
                                     max_length=200,
                                     blank=True,
                                     )
    work_address1 = models.CharField('Address Line 1',
                                     max_length=200,
                                     blank=True,
                                     )
    work_address2 = models.CharField('Address Line 2',
                                     max_length=200,
                                     blank=True,
                                     )
    work_address3 = models.CharField('Address Line 3',
                                     max_length=200,
                                     blank=True,
                                     )
    work_address4 = models.CharField('Address Line 4',
                                     max_length=200,
                                     blank=True,
                                     )
    work_address_city = models.CharField('City',
                                         max_length=60,
                                         blank=True,
                                         )
    work_address_state_county = models.CharField('State/County',
                                                 max_length=60,
                                                 blank=True,
                                                 )
    work_address_postcode = models.CharField('State/County',
                                             max_length=60,
                                             blank=True,
                                             )
    work_address_country = models.CharField('Country',
                                            max_length=60,
                                            blank=True,
                                            )
    work_Role = models.CharField('Work Designation',
                                 max_length=200,
                                 blank=True,
                                 )
    website = models.URLField('Website',
                              blank=True,
                              )
    phone_number = models.CharField(
        'Phone number',
        max_length=20,
        blank=True,
    )
    mobile_number = models.CharField(
        'Mobile number',
        max_length=20,
    )

    class ContactPreferenceChoices(models.TextChoices):
        Phone = 'PHONE', _('Landline')
        Mobile = 'MOBILE.', _('Mobile')
        Email = 'EMAIL', _('Email')
        SMS = 'SMS', _('SMS')
        Post = 'POST', _('Post')
    preferred_contact_preference = models.CharField('Preferred Contact Method',
                                                    max_length=20,
                                                    choices=ContactPreferenceChoices.choices,
                                                    default=ContactPreferenceChoices.Email,
                                                    blank=True,
                                                    )

    class ContactTimePreferenceChoices(models.TextChoices):
        Morning = 'Morning', _('Morning(before 9AM)')
        Work = 'MOBILE.', _('Work Hours(Between 9AM and 5PM)')
        Evening = 'EVENING', _('Evening (Between 5PM to 8PM)')
    preferred_contact_time = models.CharField('Preferred Contact Time',
                                              max_length=20,
                                              choices=ContactTimePreferenceChoices.choices,
                                              default=ContactTimePreferenceChoices.Work,
                                              )

    email = models.EmailField(
        'Email',
    )
    secondary_email = models.EmailField(
        'Secondary Email',
        blank=True,
    )

    social_media_1 = models.URLField('Social Media Profile-1',
                                     blank=True,
                                     )

    social_media_2 = models.URLField('Social Media Profile-2',
                                     blank=True,
                                     )
    social_media_3 = models.URLField('Social Media Profile-3',
                                     blank=True,
                                     )

    profile_picture = models.ImageField(
        null=True,
        blank=True,
        upload_to="Leads/profile_pictures/",
    )

    status = models.ForeignKey(
        Category,
        related_name="leads_Status",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    lead_Ratings = models.CharField('Lead Ratings',
                                    max_length=200,
                                    blank=True,
                                    )

    description = models.TextField(
        'Description',
        max_length=200,
        blank=True,
    )

    closeReason = models.TextField(
        'Lead Close Reason',
        max_length=200,
        blank=True,
    )
    external_ref1 = models.CharField(
        'external reference number 1',
        max_length=200,
        blank=True,
    )
    external_ref2 = models.CharField(
        'external reference number 2',
        max_length=200,
        blank=True,
    )
    external_ref3 = models.CharField(
        'external reference number 3',
        max_length=200,
        blank=True,
    )

    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now=True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )

    # objects = LeadManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.status}"

    class Meta:
        verbose_name = 'Leads'
        verbose_name_plural = 'Leads'

    def get_absolute_url(self):
        return reverse('leads:update', args=[self.pk])


# def handle_upload_follow_ups(instance, filename):
#     return f"lead_followups/lead_{instance.lead.pk}/{filename}"

# class FollowUp(models.Model):
#     lead = models.ForeignKey(
#         Lead,
#         related_name="followups",
#          on_delete=models.CASCADE,
#     )

#     notes = models.TextField(
#         blank=True,
#         null=True,
#     )

#     action = models.TextField(
#         blank=True,
#         null=True,
#     )

#     file = models.FileField(
#         null=True,
#         blank=True,
#         upload_to=handle_upload_follow_ups
#     )

#     dateTimeModified = models.DateTimeField(
#         'Last Modified',
#         auto_now =True,
#     )

#     dateTimeCreated = models.DateTimeField(
#         'Created',
#         auto_now_add =True,
#     )

#     def __str__(self):
#         return f"{self.lead.first_name} {self.lead.last_name}"

#     class Meta:
#         verbose_name = 'Follow-Ups'
#         verbose_name_plural = 'Follow-Ups'
