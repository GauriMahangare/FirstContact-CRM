from django.contrib.auth.models import AbstractUser
from django.core import exceptions
from django.db import models
from django.conf import settings
import logging
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from allauth.account.signals import email_confirmed
from django.core.exceptions import ObjectDoesNotExist
from organisation.models import Organisation
from payment.models import Pricing, Subscription

import stripe
logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY
class User(AbstractUser):
    """Default user for firstcontact_crm."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(
        'Name of the user',
        blank=True,
        max_length=255,
    )
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore
    class TitleChoices(models.TextChoices):
        Mr = 'Mr.', _('Mr.')
        Mrs = 'Mrs.', _('Mrs.')
        Miss = 'Miss.', _('Miss.')
        Ms = 'Ms.', _('Ms.')
        default = 'NotProvided', _('Prefer not to say')
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

    userorganization = models.ForeignKey(
        Organisation,
        verbose_name="User Work Organisation",
        null=True,
        on_delete=models.SET_NULL,
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

    is_admin = models.BooleanField(default=True)
    is_team_manager = models.BooleanField(default=False)
    is_team_member = models.BooleanField(default=False)
    is_organisation_default = models.BooleanField(default=True)
    is_profile_complete = models.BooleanField(default=False)

    stripe_customer_id = models.CharField(
        'Stripe customer id',
        max_length=50,
        blank=True,
        default='',
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={ "username": self.username
                                              }
                    )

def post_email_confirmed(request, email_address, *args, **kwargs):

    user = User.objects.get(email=email_address.email)
    if  user.is_admin:
        free_trial_pricing = get_object_or_404(Pricing, name='FreeTrial')

        subscription = Subscription.objects.create(
            user=user, 
            pricing=free_trial_pricing
        )
        try:
            stripe_customer = stripe.Customer.create(
            email=user.email
            )
        except:
            logger.critical('Stripe Customer create error')

        try: 
            stripe_subscription = stripe.Subscription.create(
            customer=stripe_customer["id"],
            items=[{'price': free_trial_pricing.stripe_price_id}],
            trial_period_days=7
            )
        except:
            logger.critical('Stripe Customer subscription create error')       

        subscription.status = stripe_subscription["status"]  # trialing
        subscription.stripe_subscription_id = stripe_subscription["id"]
        subscription.save()
        user.stripe_customer_id = stripe_customer["id"]
        user.save()

email_confirmed.connect(post_email_confirmed)

