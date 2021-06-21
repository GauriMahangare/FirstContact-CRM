from django.contrib import admin
from .models import Language

# Register your models here.
class LanguageAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "iso_name",
        "isActive",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "iso_name",
    ]

    list_display = [
        "iso_name",
        "alphanumeric2_iso639_1_code",
        "alphanumeric3_iso639_2T_code",
        "alphanumeric3_iso639_2B_code",
        "alphanumeric3_iso639_3_code",
        "isActive",
        "dateTimeModified",
    ]


admin.site.register(Language, LanguageAdmin)
