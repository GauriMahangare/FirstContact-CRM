from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL


class ProdUsageUnit(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    name = models.CharField(
        "Product Usage Unit",
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
        return "{self.name}".format(self=self)

    class Meta:
        verbose_name = "Product Usage Unit"
        verbose_name_plural = "Product Usage Unit"
