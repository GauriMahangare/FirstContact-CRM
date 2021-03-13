from organisation.models import Organisation
from django.contrib import admin
from django.contrib.admin.models import DELETION, LogEntry
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.

class OrganisationAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'work_org_name',
        'created_by',
        'is_verified',
        'is_access_enabled',
        'is_active',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'work_org_name',
    ]

    list_display = [
        'work_org_name',
        'created_by',
        'is_verified',
        'is_access_enabled',
        'is_active',
    ]
    #prepopulated_fields = {'slug': ('work_org_name',)}

admin.site.register(Organisation,OrganisationAdmin)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]
    

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"