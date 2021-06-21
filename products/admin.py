from django.contrib import admin

# Register your models here.
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = "dateTimeModified"

    # to filter the resultes by users, content types and action flags
    list_filter = [
        "name",
        "code",
        "category",
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        "name",
        "code",
        "category",
    ]

    list_display = [
        "code",
        "name",
        "category",
        "unit_price",
        "isActive",
        "quantity_in_stock",
        "dateTimeModified",
    ]


admin.site.register(Product, ProductAdmin)
