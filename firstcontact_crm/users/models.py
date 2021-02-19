from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from organisation.models import Organisation

class User(AbstractUser):
    """Default user for firstcontact_crm."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(
        'Name of the user',
        blank=True,
        max_length=255,
    )
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore
    class TitleChoices(models.TextChoices):
        Mr = 'Mr.', _('Mr.')
        Mrs = 'Mrs.', _('Mrs.')
        Miss = 'Miss.', _('Miss.')
        Ms = 'Ms.', _('Ms.')
        default = 'NotProvided', _('Prefer not to say')
    title = models.CharField(
        'Title',
        max_length=25,
        choices=TitleChoices.choices,
        default=TitleChoices.default,
    )
    first_name = models.CharField('First Name',
        max_length=60,
        blank=True,
    )
    last_name = models.CharField('Last Name',
        max_length=60,
        blank=True,
    )

    userorganization = models.ForeignKey(
        Organisation,
        verbose_name="User Work Organisation",
        blank=True,
        default=1,
        on_delete=models.CASCADE,
    )

    phone_number = models.CharField(
        'Phone number',
        max_length=20,
        blank=True,
    )
    mobile_number = models.CharField(
        'Mobile number',
        max_length=20,
    )

    is_admin = models.BooleanField(default=True)
    is_team_manager = models.BooleanField(default=False)
    is_team_member = models.BooleanField(default=False)
    is_organisation_default = models.BooleanField(default=True)
    is_profile_complete = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={ "username": self.username
                                              }
                    )

# def post_user_created_signal(sender, instance, created, **kwargs):
#     if created:
#         Organisation.objects.create(user=instance)


# post_save.connect(post_user_created_signal, sender=User)

# def pre_user_created_signal(sender, instance, created, **kwargs):
#     if created:
#         Organisation.objects.create(user=instance)

# pre_save.connect(pre_user_created_signal, sender=User)