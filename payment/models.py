from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from allauth.account.signals import email_confirmed
import stripe
#from feature.models import Flag
import pytz
# Create your models here.

stripe.api_key = settings.STRIPE_SECRET_KEY

User = settings.AUTH_USER_MODEL
utc=pytz.UTC
year_dropdown = []
for y in range(datetime.now().year, (datetime.now().year + 11)):
    year_dropdown.append((str(y), str(y)))

month_dropdown = []
current_month = datetime.now().month + 1

for m in range(current_month, 13):
    month_dropdown.append((str(m), str(m)))

class Pricing(models.Model):

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True,unique=True)
    class PricingTierChoices(models.TextChoices):
        Free = 'FreeTrial', _('Free Trial')
        FreeForLife = 'FreeForLife', _('Free For Life')
        Basic = 'Basic', _('Basic')
        Essential = 'Essential', _('Essential')
        Enterprise = 'Enterprise', _('Enterprise')
        Individual = 'Individual', _('Individual')
        Team = 'Team', _('Team')
        Organisation = 'Organisation', _('Organisation')

    name = models.CharField(
        'Pricing Type',
        max_length=100,
        choices=PricingTierChoices.choices,
        default=PricingTierChoices.Free,
    )  # Basic / Pro / Premium

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
    # features = models.ForeignKey(
    #     Flag,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     help_text=_('Features in this Price Tier.'),
    #     verbose_name=_('Features'),
    # )
    description = models.TextField(
        'Description',
        blank=True,
        max_length=4000,
    )
    is_default = models.BooleanField(
        default=False,
        blank=True
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
        return self.name

    # def get_absolute_url(self):
    #     return reverse('pricing-details', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Pricing'
        verbose_name_plural = 'Pricing'

class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(null=True,unique=True)

    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions')

    stripe_subscription_id = models.CharField(
        'Stripe subscription Id',
        max_length=50,
        blank=True,
    )

    status = models.CharField(
        'Subscription Status',
        max_length=100,
        blank=True,)

    period_start = models.DateTimeField(
        'Period Start Date',
        null=True,
    )

    period_end = models.DateTimeField(
        'Period End Date',
        null=True,
    )

    payment_status = models.CharField(
        'Payment Status',
        max_length=50,
        blank=True,
    )

    freeTrialEndDate = models.DateTimeField(
        'Free Trial End Date',
        null=True,
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
        return self.pricing.name

    def get_absolute_url(self):
        return reverse('subscription-details', kwargs={'pk': self.organisation})

    @property
    def is_active(self):
        return self.status == "active"

    @property
    def isTrialActive(self):
        now = datetime.now()
        nowDate = now.replace(tzinfo=utc)
        trialEndDate = self.freeTrialEndDate
        if  trialEndDate > nowDate :
            return True
        else:
            return False
    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'


class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    stripe_payment_method_id = models.CharField(
        'Stripe payment Method Id',
        max_length=50,
        blank=True,
    )

    type = models.CharField(
        'Type of card',
        max_length=60,
        blank=True,)

    brand = models.CharField(
        'Card Brand',
        max_length=60,
        blank=True,)

    country = models.CharField(
        'Card country',
        max_length=60,
        blank=True,)

    class MonthChoice(models.TextChoices):
        one = '01', _('1')
        two = '02', _('2')
        three = '03', _('3')
        four = '04', _('4')
        five = '05', _('5')
        six = '06', _('6')
        seven = '07', _('7')
        eight = '08', _('8')
        nine = '09', _('9')
        ten = '10', _('10')
        eleven = '11', _('11')
        twelve = '12', _('12')

    expiry_month = models.CharField(
        'Card Expiry Month',
        choices=month_dropdown,
        max_length=2,
        blank=True,)

    expiry_year = models.CharField(
        'Card Expiry Year',
        choices=year_dropdown,
        max_length=4,
        blank=True,
    )

    last4 = models.CharField(
        'Last 4 Digits',
        max_length=4,
        blank=True,)

    fingerprint= models.CharField(
        'Unique card finger print',
        max_length=60,
        blank=True,)

    cardId= models.CharField(
        'card Id',
        max_length=60,
        blank=True,)

    is_default = models.BooleanField(default=True)

    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )
    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('subscription-details', kwargs={'pk': self.organisation})


def create_slug(instance,new_slug=None):
    # Remove spaces and replace it by -
    slug = slugify(instance.name)

    if new_slug is not None:
        slug = new_slug

    qs = Pricing.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug )
    return slug


def pre_save_pricing_create_slug(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_pricing_create_slug,sender=Pricing)