from django.contrib import admin
from .models import VatRate

# Register your models here.
class VATrateAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = ["rate", "organisation"]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "description",
        "rate",
    ]

    list_display = [
        "organisation",
        "description",
        "rate",
        "created_by",
    ]

    # prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(VatRate, VATrateAdmin)
