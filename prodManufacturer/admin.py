from django.contrib import admin

# Register your models here.
from .models import Manufacturer

# Register your models here.
class ManufacturerAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "is_active",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "name",
        "address",
        "is_active",
    ]

    list_display = [
        "name",
        "is_active",
        "dateTimeModified",
    ]


admin.site.register(Manufacturer, ManufacturerAdmin)
