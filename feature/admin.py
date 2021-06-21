from payment.models import Pricing
from django.contrib import admin

# Register your models here.
from waffle.admin import FlagAdmin as WaffleFlagAdmin
from .models import Flag

# class PricingInline(admin.TabularInline):
#     model = Pricing


class FlagAdmin(WaffleFlagAdmin):
    list_filter = ('everyone', 'superusers', 'staff', 'authenticated','pricings',)
    

admin.site.register(Flag, FlagAdmin)
