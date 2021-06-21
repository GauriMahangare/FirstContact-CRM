from django.contrib import admin

# Register your models here.
from .models import ProdUsageUnit

# Register your models here.
class ProdUsageUnitAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "name",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "name",
    ]

    list_display = [
        "name",
        "dateTimeModified",
    ]


admin.site.register(ProdUsageUnit, ProdUsageUnitAdmin)
