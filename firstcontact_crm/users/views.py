from django.http import response
from payment.models import Pricing, PaymentMethod, Subscription
from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.forms import BaseForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
import logging
from django.views.generic.base import View
from django.views.generic.edit import CreateView, FormView
import waffle
from django.http import Http404
from waffle.decorators import waffle_flag, flag_is_active
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
    fields = [
        "email",
        "title",
        "first_name",
        "last_name",
        "phone_number",
        "mobile_number",
        "country",
        "language",
        "profile_picture",
    ]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user

    def form_valid(self, form: BaseForm) -> HttpResponse:
        user = form.save(commit=False)
        if not user.first_name:
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
                if user.first_name and user.last_name and user.mobile_number:
                    user.is_profile_complete = True
                user.save()
            except Exception as e:
                print(str(e))
                logger.critical("Error updating user profile")
                raise Http404(
                    "There was an error updating your profile. If the error persists, please try again after sometime."
                )
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["user"]
        if user.is_admin:
            # Sync with Stripe
            try:
                customer_subscription = stripe.Subscription.retrieve(
                    user.subscription.stripe_subscription_id
                )
            except Exception as e:
                print(str(e))
                logger.warning("Customer Subscription not found.")
            else:
                context["billing_thresholds"] = customer_subscription[
                    "billing_thresholds"
                ]
                context["cancel_at"] = customer_subscription["cancel_at"]
                context["cancel_at_period_end"] = customer_subscription[
                    "cancel_at_period_end"
                ]
                context["canceled_at"] = customer_subscription["canceled_at"]
                context["collection_method"] = customer_subscription[
                    "collection_method"
                ]
                context["current_period_end"] = datetime.utcfromtimestamp(
                    customer_subscription["current_period_end"]
                ).strftime("%d %B %Y")
                context["current_period_start"] = datetime.utcfromtimestamp(
                    customer_subscription["current_period_start"]
                ).strftime("%d %B %Y")
                context["days_until_due"] = customer_subscription["days_until_due"]
                context["default_payment_method"] = customer_subscription[
                    "default_payment_method"
                ]
                context["discount"] = customer_subscription["discount"]
                context["ended_at"] = customer_subscription["ended_at"]
                # context['trial_start'] = datetime.utcfromtimestamp(customer_subscription['trial_start']).strftime('%d %B %Y')
                # context['trial_end'] = datetime.utcfromtimestamp(customer_subscription['trial_end']).strftime('%d %B %Y')
                context["trial_start"] = user.date_joined
                context["trial_end"] = user.subscription.freeTrialEndDate
                context["status"] = customer_subscription["status"]
                stripe_price_id = customer_subscription["plan"]["id"]
                pricing = Pricing.objects.get(stripe_price_id=stripe_price_id)
                context["pricing_name"] = pricing.name
                # if (customer_subscription['status'] != "canceled"):
                # items  = customer_subscription['items']
                # data_list = items['data']
                # data = data_list[0]
                # price = data['price']
                # context['pricing_type'] = price['type']
                # context['unit_amount'] = '%.2f' % (price['unit_amount']/100)
                # context['currency'] = price['currency']

                pmt_method_qs = PaymentMethod.objects.filter(user=user)
                context["pmt_method_qs"] = pmt_method_qs

                # Retreive Latest Invoice status for the user from Stripe
                customer_id = user.stripe_customer_id
                try:
                    customerInvoiceList = stripe.Invoice.list(customer=customer_id)
                    print(customerInvoiceList)
                    context["customer_invoice_list"] = customerInvoiceList["data"]
                except Exception as e:
                    print(str(e))
                    logger.critical("No invoice found for {customer_id} - ", exc_info=1)

        return context

    def get(self, request, *args, **kwargs):
        previous_url = self.request.META.get("HTTP_REFERER")
        return super().get(request, *args, **kwargs)


user_subscription_view = UserSubscriptionView.as_view()


class CancelSubscriptionView(LoginRequiredMixin, View):
    # form_class = CancelSubscriptionForm

    def get_success_url(self):
        return reverse(
            "users:subscription", kwargs={"username": self.request.user.username}
        )

    def get(self, request, *args, **kwargs):
        context = {
            "subscription": self.request.user.subscription.pricing.name,
            "object": self.request.user,
            "subscriptionId": self.request.user.subscription.stripe_subscription_id,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, "users/user_confirm_subscription_cancel.html", context)

    # def post(self, request, *args, **kwargs):
    #     try:
    #         print("*** in delete subscritption***")
    #         print(self.request.user.subscription.stripe_subscription_id)
    #         # Cancel the subscription by deleting it
    #         deletedSubscription = stripe.Subscription.delete(self.request.user.subscription.stripe_subscription_id)
    #         # return jsonify(subscription=deletedSubscription)
    #         print(deletedSubscription)
    #         messages.success(self.request, "You have successfully cancelled your subscription")
    #         return reverse("users:subscription", kwargs={"username": self.request.user.username})
    #     except Exception as e:
    #         logger.critical('Customer Subscription Deletion Error')
    #         messages.error(self.request, "There was an error cancelling your subscription. Please try again later.")
    #         return jsonify(error=str(e)), 403


user_subscription_cancel_view = CancelSubscriptionView.as_view()


class PaymentMethodUpdateView(LoginRequiredMixin, SuccessMessageMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # if waffle.flag_is_active(self.request, 'update_payment_method'):
        payment_method_qs = PaymentMethod.objects.filter(user=request.user)
        for pm in payment_method_qs:
            pm.is_default = False
            pm.save()
        try:
            payment_method = PaymentMethod.objects.get(pk=pk)
            payment_method.is_default = True
            payment_method.save()
        except Exception as e:
            print(str(e))
            logger.critical("Payment Method Update error")
            raise Http404(
                "There was an error updating your payment method. If the error persists, please try again after sometime."
            )
        else:
            customer_id = request.user.stripe_customer_id
            try:
                stripe.Customer.modify(
                    customer_id,
                    invoice_settings={
                        "default_payment_method": payment_method.stripe_payment_method_id,
                    },
                )
            except Exception as e:
                print(str(e))
                logger.critical(
                    "Stripe default payment method update error", exc_info=1
                )
                return e
            else:
                messages.success(
                    self.request, "Payment method has been set as default."
                )
                # return reverse("users:subscription", kwargs={"username": self.request.user.username})
                return HttpResponseRedirect("/users/~subscription/redirect/")
        # else:
        #    messages.error(self.request, "Please update your subscription to continue using this feature.")
        #    return super(PaymentMethodUpdateView, self).form_valid(form)


PaymentMethod_update_view = PaymentMethodUpdateView.as_view()


class UserSubscriptionRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse(
            "users:subscription", kwargs={"username": self.request.user.username}
        )


user_subscription_redirect_view = UserSubscriptionRedirectView.as_view()


class PaymentMethodAddView(LoginRequiredMixin, SuccessMessageMixin, View):
    def post(self, request, pk, *args, **kwargs):
        # if waffle.flag_is_active(self.request, 'update_payment_method'):
        payment_method_qs = PaymentMethod.objects.filter(user=request.user)
        for pm in payment_method_qs:
            pm.is_default = False
            pm.save()
        try:
            payment_method = PaymentMethod.objects.get(pk=pk)
            payment_method.is_default = True
            payment_method.save()
        except Exception as e:
            print(str(e))
            logger.critical("Payment Method Update error")
            raise Http404(
                "There was an error updating your payment method. If the error persists, please try again after sometime."
            )
        else:
            messages.success(self.request, "Payment method has been set as default.")
            # return reverse("users:subscription", kwargs={"username": self.request.user.username})
            return HttpResponseRedirect("/users/~subscription/redirect/")
        # else:
        #    messages.error(self.request, "Please update your subscription to continue using this feature.")
        #    return super(PaymentMethodUpdateView, self).form_valid(form)


PaymentMethod_add_view = PaymentMethodAddView.as_view()
