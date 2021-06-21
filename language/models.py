from django.db import models

from django.conf import settings
from currency.models import Currency

# Create your models here.
User = settings.AUTH_USER_MODEL


class Language(models.Model):
    # ISO 3166
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="language_addedby"
    )

    iso_name = models.CharField(
        "ISO Language Name",
        max_length=400,
    )
    native_name = models.CharField(
        "Native name",
        max_length=400,
        blank=True,
    )

    alphanumeric2_iso639_1_code = models.CharField(
        "ISO639-1 ISO Language code",
        max_length=2,
    )
    alphanumeric3_iso639_2T_code = models.CharField(
        "ISO639-2T ISO Language code",
        max_length=3,
    )
    alphanumeric3_iso639_2B_code = models.CharField(
        "ISO639-2B ISO Language code",
        max_length=3,
    )
    alphanumeric3_iso639_3_code = models.CharField(
        "ISO639-3 ISO Language code",
        max_length=10,
        blank=True,
    )

    description = models.TextField(blank=True)

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
        return "{self.alphanumeric2_iso639_1_code}-{self.iso_name}".format(self=self)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Language"
