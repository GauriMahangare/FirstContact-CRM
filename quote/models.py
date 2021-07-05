from leads.models import Lead
from vatRate.models import VatRate
from language.models import Language
from import_export import resources
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
from currency.models import Currency
from country.models import Country
from product.models import Product
from industry.models import Industry
from category.models import Category

# from leads.admin import LeadResource
from django.urls import reverse
from django.template.loader import render_to_string

# Create your models here.

User = settings.AUTH_USER_MODEL

# Create your models here.


def quote_attachment_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    org_name = instance.organisation.work_org_name
    org_name_no_space = org_name.replace(" ", "")

    return "org_{0}/quote/{1}/quote_attachments/{3}".format(
        org_name_no_space, instance.id, filename
    )


class Stage(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        "status",
        max_length=200,
    )
    description = models.TextField(
        "Description",
        blank=True,
    )
    dateTimeModified = models.DateTimeField(
        "Last Modified",
        auto_now=True,
    )

    dateTimeCreated = models.DateTimeField(
        "Created",
        auto_now_add=True,
    )

    def __str__(self):
        return "{self.status}".format(self=self)

    class Meta:
        verbose_name = "Quote Stage"
        verbose_name_plural = "Quote Stages"


class Quote(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        serialize=False,
        auto_created=True,
        unique=True,
        editable=False,
    )
    quote_id = models.CharField("Quote ID", max_length=100, default="EST-")
    reference = models.CharField(
        "Reference",
        max_length=200,
        blank=True,
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="quote_added_by"
    )

    modified_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="quote_modified_by"
    )

    owner = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="quote_owned_by"
    )

    deal_name = models.CharField(
        "Deal Name",
        max_length=200,
    )

    subject = models.CharField(
        "Subject",
        max_length=200,
    )

    start_date = models.DateField(
        " Valid from",
        default=timezone.now,
    )
    end_date = models.DateField(
        " Valid to",
        default=timezone.now,
    )

    stage = models.ForeignKey(Stage, null=True, on_delete=models.SET_NULL)

    class contactChoices(models.TextChoices):
        lead = "Lead", _("lead")
        contact = "Contact", _("contact")
        account = "Account", _("account")

    contactType = models.CharField(
        "Contact Type",
        max_length=25,
        choices=contactChoices.choices,
        default=None,
    )

    leadId = models.ForeignKey(Lead, null=True, on_delete=models.SET_NULL)

    class TitleChoices(models.TextChoices):
        Mr = "Mr.", _("Mr.")
        Mrs = "Mrs.", _("Mrs.")
        Miss = "Miss.", _("Miss.")
        Ms = "Ms.", _("Ms.")
        default = "", _("Prefer not to say")

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
        "First Name",
        max_length=60,
    )

    work_org_name = models.CharField(
        "Work organisation",
        max_length=200,
    )
    email = models.EmailField(
        "Email",
    )
    billing_address1 = models.CharField(
        "Address Line 1",
        max_length=200,
    )
    billing_address2 = models.CharField(
        "Address Line 2",
        max_length=200,
        blank=True,
    )
    billing_address3 = models.CharField(
        "Address Line 3",
        max_length=200,
        blank=True,
    )
    billing_address4 = models.CharField(
        "Address Line 4",
        max_length=200,
        blank=True,
    )
    billing_address_city = models.CharField(
        "City",
        max_length=60,
    )
    billing_address_state_county = models.CharField(
        "State/County",
        max_length=60,
        blank=True,
    )
    billing_address_postcode = models.CharField(
        "State/County",
        max_length=60,
    )
    billing_address_country = models.ForeignKey(
        Country,
        null=True,
        on_delete=models.SET_NULL,
        related_name="billing_country",
    )
    shipping_address1 = models.CharField(
        "Address Line 1",
        max_length=200,
        blank=True,
    )
    shipping_address2 = models.CharField(
        "Address Line 2",
        max_length=200,
        blank=True,
    )
    shipping_address3 = models.CharField(
        "Address Line 3",
        max_length=200,
        blank=True,
    )
    shipping_address4 = models.CharField(
        "Address Line 4",
        max_length=200,
        blank=True,
    )
    shipping_address_city = models.CharField(
        "City",
        max_length=60,
        blank=True,
    )
    shipping_address_state_county = models.CharField(
        "State/County",
        max_length=60,
        blank=True,
    )
    shipping_address_postcode = models.CharField(
        "State/County",
        max_length=60,
        blank=True,
    )
    shipping_address_country = models.ForeignKey(
        Country,
        null=True,
        on_delete=models.SET_NULL,
        related_name="shipping_country",
    )

    terms_conditions = models.TextField(blank=True, max_length=400)
    notes = models.TextField(blank=True, max_length=400)

    currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL)

    sub_total_amount = models.DecimalField(
        "Sub Total", max_digits=11, decimal_places=2, default=0
    )
    discount = models.DecimalField(
        "Discount", max_digits=11, decimal_places=2, default=0
    )
    shipping_charges = models.DecimalField(
        "Shipping Charges", max_digits=11, decimal_places=2, default=0
    )
    shipping_vat = models.ForeignKey(
        VatRate, default=0, null=True, on_delete=models.SET_NULL
    )
    adjustment = models.DecimalField(
        "Shipping Charges", max_digits=11, decimal_places=2, default=0
    )
    total_amount = models.DecimalField(
        "Total", max_digits=11, decimal_places=2, default=0
    )
    file = models.FileField(
        null=True, blank=True, upload_to=quote_attachment_directory_path
    )

    dateTimeModified = models.DateTimeField(
        "Last Modified",
        auto_now=True,
    )

    dateTimeCreated = models.DateTimeField(
        "Created",
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.work_org_name}"

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"

    def get_absolute_url(self):
        return reverse("quote:detail", args=[self.id])


class QuotedItem(models.Model):
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="quoteItem_added_by"
    )

    modified_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="quoteItem_modified_by"
    )
    quote = models.ForeignKey(
        Quote, related_name="quoted_items", on_delete=models.CASCADE
    )
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        "Quantity",
        default=1,
    )
    amount = models.DecimalField(
        "Cost of items", default=0, max_digits=11, decimal_places=2
    )
    currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL)
    discount = models.DecimalField(
        "Discount", default=0, null=True, max_digits=11, decimal_places=2
    )

    vat_rate = models.ForeignKey(VatRate, null=True, on_delete=models.SET_NULL)
    line_total = models.DecimalField(
        "Total", default=0, max_digits=11, decimal_places=2
    )
    dateTimeModified = models.DateTimeField(
        "Last Modified",
        auto_now=True,
    )

    dateTimeCreated = models.DateTimeField(
        "Created",
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.item.id} - {self.item.name}"

    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"

    def get_absolute_url(self):
        return reverse("quote:detail", args=[self.id])
