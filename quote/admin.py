from django.contrib import admin

from .models import Quote, QuotedItem, Stage

# Register your models here.
class StageAdmin(admin.ModelAdmin):
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


admin.site.register(Stage, StageAdmin)


class QuotedItemInline(admin.TabularInline):
    model = QuotedItem
    autocomplete_fields = ["item"]


class QuoteAdmin(admin.ModelAdmin):
    inlines = [QuotedItemInline]
    list_display = (
        "id",
        "quote_id",
        "organisation",
        "start_date",
        "end_date",
        "stage",
        "total_amount",
    )
    list_filter = ["quote_id", "stage"]
    date_hierarchy = "dateTimeModified"
    search_fields = ["quote_id", "organisation", "reference"]


admin.site.register(Quote, QuoteAdmin)
