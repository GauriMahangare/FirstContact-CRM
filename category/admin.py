from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = ["status", "organisation"]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "description",
        "status",
    ]

    list_display = [
        "organisation",
        "status",
        "description",
        "created_by",
    ]

    # prepopulated_fields = {'slug': ('work_org_name',)}


admin.site.register(Category, CategoryAdmin)
