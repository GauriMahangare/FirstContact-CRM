from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
import logging
from django.views.generic.base import View
from django.views.generic.edit import CreateView, FormView
import waffle
from django.http import Http404
from waffle.decorators import waffle_flag,flag_is_active
from waffle.mixins import WaffleFlagMixin

import stripe
from django.conf import settings
import json
from datetime import datetime
from .forms import CancelSubscriptionForm
from flask import Flask, render_template, jsonify, request, send_from_directory

User = get_user_model()
logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self):
        return self.request.user

user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["email","title","first_name","last_name","phone_number","mobile_number",]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user

    def form_valid(self, form: BaseForm) -> HttpResponse:
        user = form.save(commit=False)
        if  not user.first_name:
            messages.error(self.request, "First Name is required")
            return super(UserUpdateView, self).form_valid(form)
        elif not user.last_name:
            messages.error(self.request, "Last Name is required")
            return super(UserUpdateView, self).form_valid(form)
        elif not user.mobile_number:
            messages.error(self.request, "Mobile number is required")
            return super(UserUpdateView, self).form_valid(form)
        else:
            try:
                if (user.first_name and user.last_name and user.mobile_number):
                    user.is_profile_complete=True
                user.save()
            except :
                logger.critical('Error updating user profile')
                raise Http404 ("There was an error updating your profile. If the error persists, please try again after sometime.")
        return super(UserUpdateView, self).form_valid(form)

user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserSubscriptionView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/user_subscription.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print (context)
        print (context['user'])
        user = context['user']
        print (user.subscription.stripe_subscription_id)
        if user.is_admin:
        # Sync with Stripe
            try:
                customer_subscription = stripe.Subscription.retrieve(user.subscription.stripe_subscription_id)
            except:
                logger.critical('Customer Subscription not found.')
                print(user.subscription.stripe_subscription_id)
            else:
                context['billing_thresholds'] = customer_subscription['billing_thresholds']
                context['cancel_at'] = customer_subscription['cancel_at']
                context['cancel_at_period_end'] = customer_subscription['cancel_at_period_end']
                context['canceled_at'] = customer_subscription['canceled_at']
                context['collection_method'] = customer_subscription['collection_method']
                context['current_period_end'] = datetime.utcfromtimestamp(customer_subscription['current_period_end']).strftime('%d %B %Y')
                context['current_period_start'] = datetime.utcfromtimestamp(customer_subscription['current_period_start']).strftime('%d %B %Y')
                context['days_until_due'] = customer_subscription['days_until_due']
                context['default_payment_method'] = customer_subscription['default_payment_method']
                context['discount'] = customer_subscription['discount']
                context['ended_at'] = customer_subscription['ended_at']
                context['trial_start'] = datetime.utcfromtimestamp(customer_subscription['trial_start']).strftime('%d %B %Y')
                context['trial_end'] = datetime.utcfromtimestamp(customer_subscription['trial_end']).strftime('%d %B %Y')
                context['status'] = customer_subscription['status']
                # if (customer_subscription['status'] != "canceled"):
                items  = customer_subscription['items']
                data_list = items['data']
                data = data_list[0]
                price = data['price']
                print(context['current_period_end'])
                print(context['current_period_start'])
                context['pricing_type'] = price['type']
                context['unit_amount'] = '%.2f' % (price['unit_amount']/100)
                context['currency'] = price['currency']
                
        return context


user_subscription_view = UserSubscriptionView.as_view()

class CancelSubscriptionView(LoginRequiredMixin,View):
    # form_class = CancelSubscriptionForm

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})
    
    def get(self, request, *args, **kwargs):
        context={"subscription": self.request.user.subscription.pricing.name}
        return render(request,'users/user_confirm_subscription_cancel.html',context)

    def post(self, request, *args, **kwargs):
        try:
            print("*** in delete subscritption***")    
            print(self.request.user.subscription.stripe_subscription_id)
            # Cancel the subscription by deleting it
            deletedSubscription = stripe.Subscription.delete(self.request.user.subscription.stripe_subscription_id)
            # return jsonify(subscription=deletedSubscription)
            print(deletedSubscription)
            messages.success(self.request, "You have successfully cancelled your subscription")
            return reverse("users:subscription", kwargs={"username": self.request.user.username})
        except Exception as e:
            logger.critical('Customer Subscription Deletion Error')
            messages.error(self.request, "There was an error cancelling your subscription. Please try again later.")
            return jsonify(error=str(e)), 403


user_subscription_cancel_view = CancelSubscriptionView.as_view()

class UpdateSubscriptionView(LoginRequiredMixin,View):
    # form_class = CancelSubscriptionForm

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})
    
    # def get(self, request, *args, **kwargs):
    #     context={"subscription": self.request.user.subscription.pricing.name}
    #     return render(request,'users/user_confirm_subscription_cancel.html',context)

    def post(self, request, *args, **kwargs):
        try:
            print("*** in delete subscritption***")    
            print(self.request.user.subscription.stripe_subscription_id)
            subscription = stripe.Subscription.retrieve(self.request.user.subscription.stripe_subscription_id)
            stripe.Subscription.modify(self.request.user.subscription.stripe_subscription_id,
                items=[{'price': 'price_1ISWBkFJjGPNRnAA2NzmnFUl'}],
            )
            messages.success(self.request, "You have successfully updated your subscription")
            return reverse("users:subscription", kwargs={"username": self.request.user.username})
        except Exception as e :
            logger.critical('Customer Subscription Update Error')
            messages.error(self.request, "There was an error updating your subscription. Please try again later.")
            return jsonify(error=str(e)), 403

user_subscription_update_view = UpdateSubscriptionView.as_view()
