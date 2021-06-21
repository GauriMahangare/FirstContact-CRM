from language.models import Language
from django.db import models

from django.conf import settings
from currency.models import Currency

# Create your models here.
User = settings.AUTH_USER_MODEL


class Country(models.Model):
    # ISO 3166
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="country_addedby"
    )

    name = models.CharField(
        "Name of the country",
        max_length=200,
    )
    official_name = models.CharField(
        "Official Name of the country",
        max_length=300,
    )

    alphanumeric2_iso_code = models.CharField(
        "Alpha-2 ISO Country code",
        max_length=2,
    )

    alphanumeric3_iso_code = models.CharField(
        "Alpha-3 ISO Country code",
        max_length=3,
    )

    numeric_iso_code = models.IntegerField(
        "Numeric-3 country code",
    )
    internet_root_zone_id = models.CharField(
        "Internet root zone id",
        max_length=8,
        blank=True,
    )
    currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)

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
        return "{self.alphanumeric3_iso_code}-{self.name}".format(self=self)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Country"
