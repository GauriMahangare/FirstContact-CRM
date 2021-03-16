from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.
from teams.models import Team,TeamMembership


# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'organisation',
        'name',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'name',
        'organisation'
    ]

    list_display = [
        'name',
        'organisation',
        'description',
        'count_of_members',
        'dateTimeModified',
        'dateTimeCreated',
    ]
class TeamMembershipAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'team',
        'member',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'team',
        'member'
    ]

    list_display = [
        'team',
        'member',
        'role',
        'member_username',
        'member_email',
        'team_organisation',
        'member_organisation',
        'users_in_same_org',
        'dateTimeModified',
        'dateTimeCreated',
    ]
admin.site.register(Team,TeamAdmin)
admin.site.register(TeamMembership,TeamMembershipAdmin)
