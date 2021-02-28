from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.signals import user_logged_in
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from allauth.account.signals import email_confirmed
import stripe
from organisation.models import Organisation
# Create your models here.

stripe.api_key = settings.STRIPE_SECRET_KEY

User = settings.AUTH_USER_MODEL

class Pricing(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class PricingTierChoices(models.TextChoices):
        Free = 'FreeTrial', _('Free Trial')
        Basic = 'Basic', _('Basic')
        Essential = 'Essential', _('Essential')
        Enterprise = 'Enterprise', _('Enterprise')

    name = models.CharField(
        'Pricing Type',
        max_length=100,
        choices=PricingTierChoices.choices,
        default=PricingTierChoices.Free,
    )  # Basic / Pro / Premium
    
    slug = models.SlugField()

    stripe_price_id = models.CharField(        
        'Pricing Tier Stripe Id',
        max_length=100,
        blank=True,
    )
    price = models.DecimalField(
        'Price',
        decimal_places=2, 
        max_digits=5,
    )
    currency = models.CharField(
        'Currency',
        max_length=50,
        blank=True,
    )
    # subscription = models.ForeignKey(
    #     Flag,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     help_text=_('Features in this Price Tier.'),
    #     verbose_name=_('Features'),
    # )
        
    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('pricing-details', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Pricing'
        verbose_name_plural = 'Pricing'

class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions')
    
    stripe_subscription_id = models.CharField(
        'Stripe subscription Id',
        max_length=50,
        blank=True,
    )

    status = models.CharField(
        'Status',
        max_length=100,
        blank=True,)

    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )
    def __str__(self):
        return self.user.email
    
    def get_absolute_url(self):
        return reverse('subscription-details', kwargs={'pk': self.organisation})

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    @property
    def is_active(self):
        return self.status == "active" or self.status == "trialing"
