from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from organisation.models import Organisation

User = settings.AUTH_USER_MODEL

# Create your models here.
class VatRate(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )

    description = models.CharField(
        "Description",
        blank=True,
        max_length=100,
    )
    rate = models.DecimalField("VAT Rate %", max_digits=9, decimal_places=2)
    dateTimeModified = models.DateTimeField(
        "Last Modified",
        auto_now=True,
    )

    dateTimeCreated = models.DateTimeField(
        "Created",
        auto_now_add=True,
    )

    def __str__(self):
        return "{self.description} - {self.rate}".format(self=self)

    class Meta:
        verbose_name = "VAT Rate"
        verbose_name_plural = "VAT Rates"
