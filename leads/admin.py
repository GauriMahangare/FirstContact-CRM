from django.contrib import admin
from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from import_export_celery.admin_actions import create_export_job_action
from leads.models import Lead, Note
from leads.forms import LeadModelForm
from leads.resources import LeadResource


# Register your models here.


class LeadAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = LeadResource
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "source",
        "status",
        "organisation",
        "team",
        "assigned_to",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "description",
        "email",
    ]

    list_display = [
        "organisation",
        "team",
        "assigned_to",
        "source",
        "title",
        "first_name",
        "last_name",
        "preferred_contact_preference",
        "preferred_contact_time",
        "email",
        "status",
        "closeReason",
    ]
    form = LeadModelForm

    actions = (create_export_job_action,)  # Celery import export

    # prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(Lead, LeadAdmin)


class NoteAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "dateTimeModified",
        "dateTimeCreated",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "title",
        "notes",
    ]

    list_display = ["lead", "title", "created_by"]
    # prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(Note, NoteAdmin)
