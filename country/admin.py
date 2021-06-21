from country.models import Country
from django.contrib import admin

# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "currency",
        "isActive",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "name",
        "alphanumeric2_iso_code",
        "alphanumeric3_iso_code",
        "numeric_iso_code",
    ]

    list_display = [
        "name",
        "alphanumeric2_iso_code",
        "alphanumeric3_iso_code",
        "numeric_iso_code",
        "currency",
        "isActive",
    ]

    # prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(Country, CountryAdmin)
