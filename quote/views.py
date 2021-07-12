from django.conf import settings
import logging

from django.views.generic.detail import DetailView
from quote.forms import QuoteModelForm, QuotedItemFormSet
from typing import Any, Optional
import waffle
from django.http import HttpResponse
from django.urls.base import reverse_lazy
from django.db import transaction
from django.conf import settings as django_settings
import os
from django.http.request import HttpRequest
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView,
)
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

# from waffle.decorators import waffle_flag,flag_is_active
from waffle.mixins import WaffleFlagMixin
from django.http import Http404

from .models import Quote, QuotedItem

logger = logging.getLogger(__name__)
User = get_user_model()
# Create your views here.

##########################################################################
#########                     Quote Views                   #########
##########################################################################


class QuoteListView(LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, ListView):
    model = Quote
    template_name = "Quote/quote_list.html"
    paginate_by = 5
    waffle_flag = "detail_quote"
    context_object_name = "quote_list"

    def get_queryset(self):
        org_categories_qs = Quote.objects.filter(
            organisation=self.request.user.userorganization.id
        ).order_by("-dateTimeModified")
        return org_categories_qs


Quote_list_view = QuoteListView.as_view()


class QuoteRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse(
            "quote:list",
        )


Quote_redirect_view = QuoteRedirectView.as_view()


class QuoteCreateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, CreateView
):
    model = Quote
    form_class = QuoteModelForm
    template_name = "Quote/quote_create.html"
    waffle_flag = "create_quote"
    context_object_name = "quote"
    success_url = reverse_lazy("quote:redirect")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["user_org"] = self.request.user.userorganization
        return kwargs

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            # context["quoteform"] = QuoteModelForm(self.request.POST, self.request.FILES)
            context["formset"] = QuotedItemFormSet(
                self.request.POST,
                user=self.request.user,
                user_org=self.request.user.userorganization,
            )
        else:
            # context["quoteform"] = QuoteModelForm(self.request.GET or None)
            context["formset"] = QuotedItemFormSet(
                queryset=QuotedItem.objects.none(),
                user=self.request.user,
                user_org=self.request.user.userorganization,
            )
        return context

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "create_quote"):
            context = self.get_context_data()
            # quoteform = context["quoteform"]
            quoteform = context["form"]
            formset = context["formset"]
            if quoteform.is_valid() and formset.is_valid():
                quote = quoteform.save(commit=False)
                quote.created_by = self.request.user
                quote.organisation = self.request.user.userorganization
                try:
                    quote.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Quote Create error")
                    raise Http404(
                        "There was an error creating your quote. If the error persists, please try again after sometime."
                    )
                else:
                    subtotal = 0
                    for form in formset:
                        quotedItem = form.save(commit=False)
                        quotedItem.quote = quote
                        costprice = (quotedItem.quantity) * (quotedItem.amount)
                        discountedCost = costprice - (
                            costprice * quotedItem.discount / 100
                        )

                        if quotedItem.vat_rate is None:
                            vat_rate_rate = 0
                        else:
                            vat_rate_rate = quotedItem.vat_rate.rate

                        discountedCostVat = discountedCost + (
                            discountedCost * vat_rate_rate / 100
                        )
                        quotedItem.line_total = discountedCostVat
                        subtotal = subtotal + discountedCostVat
                        try:
                            quotedItem.save()
                        except Exception as e:
                            print(str(e))
                            logger.critical("Quoted items  create error")
                            raise Http404(
                                "There was an error creating your quote. If the error persists, please try again after sometime."
                            )
                    quote.sub_total_amount = subtotal
                    totalFinalDiscount = subtotal - (subtotal * quote.discount / 100)
                    if quote.shipping_vat is None:
                        shipping_vat_rate = 0
                    else:
                        shipping_vat_rate = quote.shipping_vat.rate

                    shippingcharge = quote.shipping_charges + (
                        quote.shipping_charges * shipping_vat_rate / 100
                    )
                    finalTotal = totalFinalDiscount + shippingcharge - quote.adjustment
                    quote.total_amount = finalTotal
                    try:
                        quote.save()
                    except Exception as e:
                        print(str(e))
                        logger.critical("Quote create 2 error")
                        raise Http404(
                            "There was an error creating your quote. If the error persists, please try again after sometime."
                        )
                    else:
                        messages.success(
                            self.request,
                            "Quote has been created successfully.",
                        )
                        return redirect(reverse("quote:list"))
            else:
                if form.errors:
                    logger.critical("Errors in Quoteform: ")
                    logger.critical(quoteform.errors)
                if formset.errors:
                    logger.critical("Errors in QuotedItemformset: ")
                    logger.critical(formset.errors)
                return self.render_to_response(
                    self.get_context_data(form=form, formset=formset)
                )
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(QuoteUpdateView, self).form_valid(form)


Quote_create_view = QuoteCreateView.as_view()


class QuoteUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, UpdateView
):
    model = Quote
    form_class = QuoteModelForm
    template_name = "Quote/quote_update.html"
    waffle_flag = "update_quote"
    context_object_name = "quote"
    success_url = reverse_lazy("quote:redirect")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["user_org"] = self.request.user.userorganization
        return kwargs

    def get_context_data(self, **kwargs: Any):
        context = super(QuoteUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            # context["quoteform"] = QuoteModelForm(
            #     self.request.POST, self.request.FILES, instance=self.object
            # )
            context["formset"] = QuotedItemFormSet(
                self.request.POST,
                instance=self.object,
                user=self.request.user,
                user_org=self.request.user.userorganization,
            )
        else:
            # context["quoteform"] = QuoteModelForm(instance=self.object)
            context["formset"] = QuotedItemFormSet(
                queryset=QuotedItem.objects.filter(quote=self.object),
                user=self.request.user,
                user_org=self.request.user.userorganization,
            )
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = QuotedItemFormSet(
            self.request.POST,
            user=self.request.user,
            user_org=self.request.user.userorganization,
        )

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        if waffle.flag_is_active(self.request, "update_quote"):
            quote = form.save(commit=False)
            quote.modified_by = self.request.user
            quote.organisation = self.request.user.userorganization
            try:
                quote.save()
            except Exception as e:
                print(str(e))
                logger.critical("Quote Update error")
                raise Http404(
                    "There was an error updating your quote. If the error persists, please try again after sometime."
                )
            else:
                subtotal = 0
                for form in formset:
                    quotedItem = form.save(commit=False)
                    quotedItem.quote = quote
                    costprice = (quotedItem.quantity) * (quotedItem.amount)
                    discountedCost = costprice - (costprice * quotedItem.discount / 100)
                    if quotedItem.vat_rate is None:
                        vat_rate_rate = 0
                    else:
                        vat_rate_rate = quotedItem.vat_rate.rate
                    discountedCostVat = discountedCost + (
                        discountedCost * vat_rate_rate / 100
                    )
                    quotedItem.line_total = discountedCostVat
                    subtotal = subtotal + discountedCostVat
                    try:
                        quotedItem.save()
                    except Exception as e:
                        print(str(e))
                        logger.critical("Quoted items  Update error")
                        raise Http404(
                            "There was an error updating your quote. If the error persists, please try again after sometime."
                        )
                quote.sub_total_amount = subtotal
                totalFinalDiscount = subtotal - (subtotal * quote.discount / 100)
                if quote.shipping_vat is None:
                    shipping_vat_rate = 0
                else:
                    shipping_vat_rate = quote.shipping_vat.rate
                shippingcharge = quote.shipping_charges + (
                    quote.shipping_charges * shipping_vat_rate / 100
                )
                finalTotal = totalFinalDiscount + shippingcharge - quote.adjustment
                quote.total_amount = finalTotal
                try:
                    quote.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Quote update 2 error")
                    raise Http404(
                        "There was an error updating your quote. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Quote has been updated successfully.",
                    )
                    return redirect(reverse("quote:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(QuoteUpdateView, self).form_valid(form, formset)

    def form_invalid(self, form, formset):
        if form.errors:
            logger.critical("Errors in Quoteform: ")
            logger.critical(form.errors)
        if formset.errors:
            logger.critical("Errors in QuotedItemformset: ")
            logger.critical(formset.errors)
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


Quote_update_view = QuoteUpdateView.as_view()


class QuoteDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, DeleteView
):
    model = Quote
    template_name = "quote/quote_confirm_delete.html"
    waffle_flag = "delete_quote"
    context_object_name = "quote"
    success_url = reverse_lazy("quote:redirect")
    success_message = _("Quote has been deleted.")

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.warning(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


Quote_delete_view = QuoteDeleteView.as_view()


class QuoteDetailView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, TemplateView
):
    model = Quote
    template_name = "quote/quote_template_detail.html"
    context_object_name = "quote"
    waffle_flag = "detail_quote"


Quote_detail_view = QuoteDetailView.as_view()


class QuoteDisplayView(QuoteDetailView):
    def get_template_names(self):
        print("== in get_template_names== ")
        print(self.request.user.userorganization.quote_template)
        print(self.request.user.userorganization.quote_template.url)
        print(self.request.user.userorganization.quote_template.name)
        print(settings.MEDIA_URL)
        print(settings.MEDIA_ROOT)
        file_name = self.request.user.userorganization.quote_template.name
        template_name = settings.MEDIA_ROOT + "\\" + file_name.replace("/", "\\")

        print(template_name)
        # template_name = template_name
        return [template_name]
        # return [template_file_path]


Quote_display_view = QuoteDisplayView.as_view()
