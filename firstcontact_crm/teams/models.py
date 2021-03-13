from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth import get_user, get_user_model
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from organisation.models import Organisation
from invitations.utils import get_invitation_model
from django.utils.translation import gettext_lazy as _
from invitations.models import Invitation

# Create your models here.
User = settings.AUTH_USER_MODEL

class Team(models.Model):
    created_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    slug = models.SlugField(null=True, unique=True)

    name = models.CharField('Team Name',
        max_length=300,
        default='',
        help_text='Team Name'
    )
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
    )
    description = models.TextField('Team Description',
        default='',
        blank=True,
        help_text='Enter Team objectives here'
    )
    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )
    @property
    def count_of_members(self):
        return TeamMembership.objects.filter(team_id=self.pk).count()

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        #return reverse('team-detail', kwargs={'pk': self.pk})
        return reverse('teams:update', kwargs={"slug_text": self.slug})

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
# Create your models here.


def create_slug(instance,new_slug=None):
    # Remove spaces and replace it by -
    slug = slugify(instance.name)

    if new_slug is not None:
        slug = new_slug
        
    qs = Team.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug )
    return slug


def pre_save_team_create_slug(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_team_create_slug,sender=Team)

User = get_user_model()
class TeamMembership(models.Model):
    
    team = models.ForeignKey(Team,null=True,on_delete=models.CASCADE)
    member = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    slug = models.SlugField(null=True, unique=True)

    class roleChoices(models.TextChoices):
        Agent = 'Agent', _('Agent')
        Teammanager = 'Teammanager', _('Team Manager')

    role = models.CharField(
        'Role',
        max_length=100,
        choices=roleChoices.choices,
        default=roleChoices.Agent,
    ) 


    dateTimeModified = models.DateTimeField(
        'Last Modified',
        auto_now =True,
    )

    dateTimeCreated = models.DateTimeField(
        'Created',
        auto_now_add =True,
    )

    @property
    def team_organisation(self):
        team =  Team.objects.get(pk=self.team_id)
        return team.organisation

    @property
    def member_username(self):
        user =  User.objects.get(pk=self.member_id)
        return user.username
    
    @property
    def member_email(self):
        user =  User.objects.get(pk=self.member_id)
        return user.email

    def __str__(self):
        return f"{self.team}"
    class Meta:
        unique_together = ('team', 'member',)
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'

def create_team_member_slug(instance,new_slug=None):
    # Remove spaces and replace it by -
    slug = slugify(instance.member)
    print("*****")
    print(instance.member)
    print(slug)
    print(new_slug)
    

    if new_slug is not None:
        slug = new_slug
        
    qs = TeamMembership.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    print(exists)
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_team_member_slug(instance, new_slug=new_slug )
    return slug


def pre_save_team_member_create_slug(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = create_team_member_slug(instance)

pre_save.connect(pre_save_team_member_create_slug,sender=TeamMembership)
