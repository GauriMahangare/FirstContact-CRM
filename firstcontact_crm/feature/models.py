from django.conf import settings
from waffle.utils import get_setting, keyfmt
from payment.models import Pricing,Subscription
from django.db import models
from waffle import managers, get_waffle_flag_model
from waffle.models import AbstractUserFlag, CACHE_EMPTY
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

# Create your models here.
# User = settings.AUTH_USER_MODEL
class Flag(AbstractUserFlag):
    ''' Customisable version of Waffle Model to have feature flags based on user subscriptions'''
    FLAG_PRICINGS_CACHE_KEY = 'FLAG_PRICINGS_CACHE_KEY'
    FLAG_PRICINGS_CACHE_KEY_DEFAULT = 'flag:%s:pricings'

    pricings = models.ManyToManyField(
        Pricing,
        # on_delete=models.CASCADE,
        blank=True,
        help_text=_('Activate this flag for users with these subscriptions'),
        verbose_name=_('Subscriptions'),
    )
    def get_flush_keys(self, flush_keys=None):
        flush_keys = super(Flag, self).get_flush_keys(flush_keys)
        pricings_cache_key = get_setting(Flag.FLAG_PRICINGS_CACHE_KEY, Flag.FLAG_PRICINGS_CACHE_KEY_DEFAULT)
        flush_keys.append(keyfmt(pricings_cache_key, self.name))
        return flush_keys
    
    def is_active_for_user(self, user):
        is_active = super(Flag, self).is_active_for_user(user)
        if is_active:
            return is_active

        usersubscription=Subscription.objects.get(user_id=user.pk)
        if  usersubscription:
            pricing_ids = self._get_pricing_ids() 
            if usersubscription.pricing_id in pricing_ids:
               return True
        else:
            print("User does not have Subscription!!")
            return False

    def _get_pricing_ids(self):
        cache_key = keyfmt(
            get_setting(Flag.FLAG_PRICINGS_CACHE_KEY, Flag.FLAG_PRICINGS_CACHE_KEY_DEFAULT),
            self.name
        )
        cached = cache.get(cache_key)
        if cached == CACHE_EMPTY:
            return set()
        if cached:
            return cached
        
        pricing_ids = set(self.pricings.all().values_list('pk', flat=True))
        if not pricing_ids:
            cache.add(cache_key, CACHE_EMPTY)
            return set()

        cache.add(cache_key, pricing_ids)
        return pricing_ids