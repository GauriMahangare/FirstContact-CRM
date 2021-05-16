from payment.models import Subscription,Pricing,PaymentMethod
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
        'period_start',
        'period_end',
        'payment_status',
        'freeTrialEndDate',
        'is_active',
        'isTrialActive',
        'dateTimeModified',
        'dateTimeCreated',
    ]
class PaymentMethodAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'brand',
        'type',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'user',
    ]

    list_display = [
        'user',
        'subscription',
        'stripe_payment_method_id',
        'type',
        'brand',
        'country',
        'expiry_month',
        'expiry_year',
        'last4',
        'is_default',
        'dateTimeModified',
        'dateTimeCreated',
    ]

class PricingAdmin(admin.ModelAdmin):
    date_hierarchy = 'dateTimeModified'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'name',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'name',
    ]

    list_display = [
        'name',
        'stripe_price_id',
        'price',
        'currency',
        'is_default',
        'dateTimeModified',
        'dateTimeCreated',
    ]


admin.site.register(Subscription,SubscriptionAdmin)
admin.site.register(Pricing,PricingAdmin)
admin.site.register(PaymentMethod,PaymentMethodAdmin)