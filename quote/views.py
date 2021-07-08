import logging
from quote.forms import QuoteModelForm, QuotedItemFormSet
from typing import Any, Optional
import waffle
from django.http import HttpResponse
from django.urls.base import reverse_lazy
from django.db import transaction

from django.http.request import HttpRequest
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import RedirectView
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
#########                     Categories Views                   #########
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

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            print("request is post")
            context["quoteform"] = QuoteModelForm(self.request.POST)
            context["formset"] = QuotedItemFormSet(self.request.POST)
            print(context["quoteform"])
            print(context["formset"])
        else:
            context["quoteform"] = QuoteModelForm(self.request.GET or None)
            context["formset"] = QuotedItemFormSet(queryset=QuotedItem.objects.none())
        return context

    def form_valid(self, form):
        print("form is valid")
        if waffle.flag_is_active(self.request, "create_quote"):
            print("feature flag active")
            context = self.get_context_data()
            print(context)
            quoteform = context["quoteform"]
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
                    for form in formset:
                        quotedItem = form.save(commit=False)
                        quotedItem.quote = quote
                        try:
                            quotedItem.save()
                        except Exception as e:
                            print(str(e))
                            logger.critical("Quoted items  Create error")
                            raise Http404(
                                "There was an error creating your quote. If the error persists, please try again after sometime."
                            )
                        else:
                            messages.success(
                                self.request,
                                "Congratulations!! Quote has been added successfully.",
                            )
                            return redirect(reverse("quote:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(QuoteCreateView, self).form_valid(form)


Quote_create_view = QuoteCreateView.as_view()


class QuoteUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, UpdateView
):
    model = Quote
    fields = ["status", "description"]
    template_name = "Quote/quote_update.html"
    waffle_flag = "update_quote"
    context_object_name = "quote"
    success_url = reverse_lazy("leads:redirectquote")

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "update_quote"):
            quote = form.save(commit=False)
            quote.created_by = self.request.user
            if not quote.status:
                messages.error(self.request, "Quote name is required")
                return super(QuoteUpdateView, self).form_valid(form)

            else:
                try:
                    quote.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Quote Update error")
                    raise Http404(
                        "There was an error creating your quote. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Congratulations!! Quote has been updated successfully.",
                    )
                    return redirect(reverse("quote:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(QuoteUpdateView, self).form_valid(form)


Quote_update_view = QuoteUpdateView.as_view()


class QuoteDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, DeleteView
):
    model = Quote
    template_name = "Quote/quote_confirm_delete.html"
    waffle_flag = "delete_quote"
    context_object_name = "quote"
    success_url = reverse_lazy("leads:redirectquote")
    success_message = _("Quote has been deleted.")

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.warning(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


Quote_delete_view = QuoteDeleteView.as_view()
