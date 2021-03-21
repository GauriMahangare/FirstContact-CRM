from payment.models import Subscription,Pricing
from django.contrib import admin

# Register your models here.

class SubscriptionAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'pricing',
        'status',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'user',
    ]

    list_display = [
        'user',
        'pricing',
        'stripe_subscription_id',
        'status',
        'nextPaymentDueDate',
        'freeTrialEndDate',
        'is_active',
        'isTrialActive',
    ]

admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Pricing)