from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.
from teams.models import Team


# Register your models here.

admin.site.register(Team)
