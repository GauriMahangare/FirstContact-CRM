from django.contrib import admin
from .models import Industry

# Register your models here.
class IndustryAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "sector",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "title",
        "sector",
    ]

    list_display = [
        "title",
        "sector",
        "description",
        "created_by",
    ]


admin.site.register(Industry, IndustryAdmin)
