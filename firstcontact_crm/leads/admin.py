from leads.models import Category, Lead, Note, Industry
from django.contrib import admin
from leads.forms import LeadModelForm

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'description',
        'created_by',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'description',
    ]

    list_display = [
        'status',
        'description',
        'created_by',
    ]

    #prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(Category, CategoryAdmin)


class IndustryAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'title',
        'created_by',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'title',
    ]

    list_display = [
        'title',
        'description',
        'created_by',
    ]


admin.site.register(Industry, IndustryAdmin)


class LeadAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'source',
        'status',
        'organisation',
        'team',
        'assigned_to',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'description',
        'email',

    ]

    list_display = [
        'organisation',
        'team',
        'assigned_to',
        'source',
        'title',
        'first_name',
        'last_name',
        'preferred_contact_preference',
        'preferred_contact_time',
        'email',
        'status',
        'closeReason',
    ]
    form = LeadModelForm
    #prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(Lead, LeadAdmin)


class NoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'dateTimeModified',
        'dateTimeCreated',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'title',
        'notes',

    ]

    list_display = [
        'lead',
        'title',
        'created_by'
    ]
    #prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(Note, NoteAdmin)
