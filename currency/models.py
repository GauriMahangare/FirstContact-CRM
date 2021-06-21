from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class Currency(models.Model):
    # ISO 4217
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    alphanumeric_iso_code = models.CharField(
        "Alpha ISO Currency code",
        max_length=3,
    )
    numeric_iso_code = models.IntegerField(
        "Numeric ISO Currency code",
    )
    description = models.CharField(
        "Description",
        max_length=100,
        blank=True,
    )
    symbol = models.CharField(
        "Symbol",
        max_length=1,
        blank=True,
    )
    decimal_sepeartor = models.IntegerField(
        "Decimal Seperator",
        default=2,
    )
    thousand_seperator = models.CharField(
        "thousand_seperator",
        max_length=1,
        blank=True,
    )
    isActive = models.BooleanField(default=True)

    dateTimeModified = models.DateTimeField(
        "Last Modified",
        auto_now=True,
    )

    dateTimeCreated = models.DateTimeField(
        "Created",
        auto_now_add=True,
    )

    def __str__(self):
        return "{self.alphanumeric_iso_code}".format(self=self)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currency"
