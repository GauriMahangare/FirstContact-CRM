from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL
# Create your models here.
class Industry(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    title = models.CharField(
        "Title",
        max_length=200,
    )
    sector = models.CharField(
        "Sector",
        blank=True,
        null=True,
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
        return "{self.title}".format(self=self)

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industry"
