from product.validators import validate_code
from currency.models import Currency
from django.db import models
from django.utils import timezone
from django.conf import settings
from organisation.models import Organisation
from prodManufacturer.models import Manufacturer
from prodCategory.models import ProdCategory
from prodUsageUnit.models import ProdUsageUnit

# Create your models here.

User = settings.AUTH_USER_MODEL


def product_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    org_name = instance.organisation.work_org_name
    org_name_no_space = org_name.replace(" ", "")
    return "org_{0}/products/{1}/{2}".format(org_name_no_space, instance.id, filename)


class Product(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        auto_created=True,
        serialize=False,
        editable=False,
    )
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="product_added_by"
    )

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=product_directory_path,
    )
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="product_owner",
    )
    handler = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="product_handler",
    )
    code = models.CharField(
        "Product Code",
        max_length=40,
        validators=[
            validate_code,
        ],
    )
    name = models.CharField(
        "Product Name",
        max_length=200,
    )
    category = models.ForeignKey(ProdCategory, null=True, on_delete=models.SET_NULL)

    isActive = models.BooleanField("Is Active", blank=True, null=True, default=True)
    manufacturer = models.ForeignKey(Manufacturer, null=True, on_delete=models.SET_NULL)

    sale_start_date = models.DateTimeField(
        "Sale start date", default=timezone.now, blank=True
    )
    sale_end_date = models.DateTimeField(
        "Sale end date", default=timezone.now, blank=True
    )
    support_start_date = models.DateTimeField(
        "Support start date", default=timezone.now, blank=True
    )
    support_end_date = models.DateTimeField(
        "Support end date", default=timezone.now, blank=True
    )
    unit_price = models.DecimalField(
        "Unit Price",
        max_digits=9,
        decimal_places=2,
        default=0.0,
    )
    currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL)

    comission_rate = models.DecimalField(
        "Comission Rate",
        max_digits=5,
        decimal_places=2,
        default=0.0,
    )
    tax = models.DecimalField(
        "Tax Rate",
        max_digits=5,
        decimal_places=2,
        default=0.0,
    )
    isTaxable = models.BooleanField(
        "Is Taxable",
        blank=True,
        null=True,
        default=False,
    )
    usage_unit = models.ForeignKey(
        ProdUsageUnit,
        null=True,
        on_delete=models.SET_NULL,
    )

    quantity_in_stock = models.IntegerField(
        "Current Stock",
        blank=True,
        default=0,
    )
    quantity_ordered = models.IntegerField(
        "Quantity Ordered",
        blank=True,
        default=0,
    )
    reorder_level = models.CharField(
        "Reorder level",
        max_length=60,
        blank=True,
    )

    quantity_in_demand = models.CharField(
        "Quantity in demand",
        max_length=60,
        blank=True,
    )
    description = models.TextField(
        "Description",
        max_length=400,
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
        return f"{self.category} {self.name}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
