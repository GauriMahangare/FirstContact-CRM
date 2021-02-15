from django.db import models
from django.db.models.deletion import SET_NULL

# Create your models here.
class Organisation(models.Model):
    work_org_name = models.CharField('Work organisation',
        max_length=300,
        blank=True,
    )
    work_Address = models.TextField('Work Address',
        blank=True,
    )
    is_verified = models.BooleanField(default=True)
    is_access_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )

    subscriptionType = models.TextField('Subscription',
        blank=True,
    )

    def __str__(self):
        return f"{self.work_org_name}"
        
    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'