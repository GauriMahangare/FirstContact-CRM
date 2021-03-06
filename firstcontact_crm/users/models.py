from language.models import Language
from country.models import Country
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.core import exceptions
from django.db import models
from django.conf import settings
import logging
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from allauth.account.signals import email_confirmed, user_signed_up, user_logged_in
from allauth.account.models import EmailAddress
from django.core.exceptions import ObjectDoesNotExist
from organisation.models import Organisation
from payment.models import Pricing, Subscription

from invitations.utils import get_invitation_model

import stripe

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


def user_profile_image_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    org_name = instance.userorganization.work_org_name
    org_name_no_space = org_name.replace(" ", "")
    return "org_{0}/users/{1}/profile_picture/{2}".format(
        org_name_no_space, instance.username, filename
    )


class User(AbstractUser):
    """Default user for firstcontact_crm."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(
        "Name of the user",
        blank=True,
        max_length=255,
    )
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore
    class TitleChoices(models.TextChoices):
        Mr = "Mr.", _("Mr.")
        Mrs = "Mrs.", _("Mrs.")
        Miss = "Miss.", _("Miss.")
        Ms = "Ms.", _("Ms.")
        default = "NotProvided", _("Prefer not to say")

    title = models.CharField(
        "Title",
        max_length=25,
        choices=TitleChoices.choices,
        default=TitleChoices.default,
    )
    first_name = models.CharField(
        "First Name",
        max_length=60,
    )
    last_name = models.CharField(
        "Last Name",
        max_length=60,
    )

    userorganization = models.ForeignKey(
        Organisation,
        verbose_name="User Work Organisation",
        null=True,
        on_delete=models.SET_NULL,
    )

    phone_number = models.CharField(
        "Phone number",
        max_length=20,
        blank=True,
    )
    mobile_number = models.CharField(
        "Mobile number",
        max_length=20,
    )
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    profile_picture = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_profile_image_directory_path,
    )

    is_admin = models.BooleanField(default=True)
    is_team_member = models.BooleanField(default=False)
    is_organisation_default = models.BooleanField(default=True)
    is_profile_complete = models.BooleanField(default=False)

    stripe_customer_id = models.CharField(
        "Stripe customer id",
        max_length=50,
        blank=True,
        default="",
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


def post_email_confirmed(request, email_address, *args, **kwargs):

    emailAddress = EmailAddress.objects.get(email=email_address.email)
    user = User.objects.get(pk=emailAddress.user.pk)

    if user.is_admin:
        try:
            user_subs = Subscription.objects.get(user=user)
        except:
            logger.info("New admin user confirmed email.")
            free_trial_pricing = get_object_or_404(Pricing, name="FreeTrial")
            try:
                subscription = Subscription.objects.create(
                    user=user, pricing=free_trial_pricing
                )
            except:
                logger.critical("user subscription creation error")
            else:
                logger.info("user subscription created successfully")
                try:
                    stripe_customer = stripe.Customer.create(email=user.email)
                except:
                    logger.critical("Stripe Customer create error")
                else:

                    # try:
                    #     stripe_subscription = stripe.Subscription.create(
                    #     customer=stripe_customer["id"],
                    #     items=[{'price': free_trial_pricing.stripe_price_id}],
                    #     trial_period_days=7
                    #     )
                    # except:
                    #     logger.critical('Stripe Customer subscription create error')

                    # subscription.status = stripe_subscription["status"]  # trialing
                    # subscription.stripe_subscription_id = stripe_subscription["id"]
                    # subscription.freeTrialEndDate = datetime.utcfromtimestamp(stripe_subscription['trial_end'])
                    # subscription.nextPaymentDueDate = datetime.utcfromtimestamp(stripe_subscription['current_period_end'])

                    # subscription.status = 'trialing'
                    logger.info("Stripe Customer created successfully")
                    subscription.freeTrialEndDate = datetime.now() + timedelta(days=7)
                    user.subscription.slug = (
                        user.username + "-" + subscription.pricing.name
                    )
                    subscription.save()

                    user.stripe_customer_id = stripe_customer["id"]
                    user.save()
        else:
            logger.info("Existing admin user confirmed new email.")
            try:
                stripe.Customer.modify(
                    user.stripe_customer_id,
                    name=emailAddress.email,
                )
            except:
                logger.critical("Stripe Customer email update error.")
            else:
                logger.info("Stripe Customer email updated successfully.")


def post_user_signed_up_checkinvitation(request, user, *args, **kwargs):
    Invitation = get_invitation_model()
    try:
        invite = Invitation.objects.get(email=user.email)
    except:
        logger.info("User is not an invited user. Register as admin")
        """
        is_admin is true
        is_organisation_default is true
        userorganization is blank
        """
    else:
        """
        is_admin is true
        is_organisation_default is true
        userorganization is blank
        """
        try:
            inviter_user = User.objects.get(pk=invite.inviter_id)
        except:
            logger.critical("Error setting up invited user - Inviter user not found")
        else:
            user.userorganization = inviter_user.userorganization
            user.is_admin = False
            user.is_team_member = True
            user.is_organisation_default = False
            try:
                user.save()
            except:
                logger.critical("Error updating invited users")
            else:
                try:
                    emailAddress = EmailAddress.objects.get(email=user.email)
                except:
                    emailAddress = EmailAddress()
                    emailAddress.user = user.pk
                    emailAddress.email = user.email
                    emailAddress.verified = True
                    emailAddress.primary = True
                    try:
                        emailAddress.save()
                    except:
                        logger.critical("Error setting up verified email")
                else:
                    logger.info("Invited users - email already verified.")


user_signed_up.connect(post_user_signed_up_checkinvitation)

email_confirmed.connect(post_email_confirmed)
