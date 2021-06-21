from currency.models import Currency
from django.contrib import admin

# Register your models here.
class CurrencyAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "alphanumeric_iso_code",
        "isActive",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "description",
        "alphanumeric_iso_code",
        "numeric_iso_code",
    ]

    list_display = [
        "alphanumeric_iso_code",
        "numeric_iso_code",
        "description",
        "isActive",
    ]

    # prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(Currency, CurrencyAdmin)
