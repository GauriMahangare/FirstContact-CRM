from django.contrib import admin
from .models import ProdCategory

# Register your models here.
class ProdCategoryAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "name",
        "description",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "title",
    ]

    list_display = [
        "name",
        "description",
        "created_by",
        "dateTimeModified",
    ]


admin.site.register(ProdCategory, ProdCategoryAdmin)
