from django.db import models
from datetime import date
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL
class Campaign(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    
    description = models.CharField(
        'Description',
        max_length=200,
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
        return "{self.description}".format(self=self)
    
    class Meta:
        verbose_name = 'Campaign'
        verbose_name_plural = 'Campaigns'

class Category(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    
    description = models.CharField(
        'Description',
        max_length=200,
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
        return "{self.description}".format(self=self)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category' 

class Agent(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
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
        return "{self.user.name}".format(self=self)
    
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agent' 

class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Lead(models.Model):
    lead_source = models.CharField('Source',
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
        blank=True,
    )
    last_name = models.CharField('Last Name',
        max_length=60,
        blank=True,
    )
    age = models.IntegerField(
        'Age',
        default=0,
    )
    work_org_name = models.CharField('Work organisation',
        max_length=200,
        blank=True,
    )
    work_Address = models.TextField('Work Address',
        blank=True,
    )
    phone_number = models.CharField(
        'Phone number',
        max_length=20,
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
    preferred_contact_preference = models.CharField('Phone number',
        max_length=20,
        choices=ContactPreferenceChoices.choices,
        blank=True,
    )

    class ContactTimePreferenceChoices(models.TextChoices):
        Morning = 'Morning', _('Morning(before 9AM)')
        Work = 'MOBILE.', _('Work Hours(Between 9AM and 5PM)')
        Evening = 'EVENING', _('Evening (Between 5PM to 8PM)')
    preferred_contact_preference = models.CharField('Phone number',
        max_length=20,
        choices=ContactTimePreferenceChoices.choices,
        default=ContactTimePreferenceChoices.Work,
    )

    email = models.EmailField(
        'Email',
        blank=True,
    )

    social_media_1 = models.CharField('Social Media Profile-1',
        max_length=200,
        blank=True,
    )

    social_media_2 = models.CharField('Social Media Profile-2',
        max_length=200,
        blank=True,
    )
    social_media_3 = models.CharField('Social Media Profile-3',
        max_length=200,
        blank=True,
    )

    profile_picture = models.ImageField(
        null=True, 
        blank=True, 
        upload_to="profile_pictures/",
    )

    lead_status = models.CharField('Lead Status',
        max_length=20,
        choices=ContactTimePreferenceChoices.choices,
        default=ContactTimePreferenceChoices.Work,
    )

    assigned_campaign = models.ForeignKey(
        Campaign, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL,
    )

    assigned_agent = models.ForeignKey(
        Agent, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL,
    )

    lead_status = models.ForeignKey(
        Category, 
        related_name="leads", 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
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

    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )

    objects = LeadManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.lead_status}"
    
    class Meta:
        verbose_name = 'Leads'
        verbose_name_plural = 'Leads'

def handle_upload_follow_ups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"

class FollowUp(models.Model):
    lead = models.ForeignKey(
        Lead, 
        related_name="followups",
         on_delete=models.CASCADE,
    )

    notes = models.TextField(
        blank=True, 
        null=True,
    )

    action = models.TextField(
        blank=True, 
        null=True,
    )

    file = models.FileField(
        null=True, 
        blank=True, 
        upload_to=handle_upload_follow_ups
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
        return f"{self.lead.first_name} {self.lead.last_name}"
    
    class Meta:
        verbose_name = 'Follow-Ups'
        verbose_name_plural = 'Follow-Ups'

