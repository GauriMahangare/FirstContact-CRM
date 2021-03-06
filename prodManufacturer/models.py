from django.db import models
from django.conf import settings
from organisation.models import Organisation

# Create your models here.
User = settings.AUTH_USER_MODEL


class Manufacturer(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        "Product Manufacturer",
        max_length=200,
    )
    address = models.TextField(
        "Contact Details",
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
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
        return "{self.name}".format(self=self)

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"
