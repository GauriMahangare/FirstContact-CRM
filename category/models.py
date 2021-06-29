from django.conf import settings
from django.db import models
from organisation.models import Organisation

User = settings.AUTH_USER_MODEL

# Create your models here.
class Category(models.Model):
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
        verbose_name = "Lead Category"
        verbose_name_plural = "Lead Category"
