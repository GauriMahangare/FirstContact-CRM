import logging
from typing import Any, Optional
from django.forms import formsets
import waffle
from django.http import HttpResponse
from django.urls.base import reverse_lazy


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

from .models import Product
from .forms import ProductModelForm

logger = logging.getLogger(__name__)
User = get_user_model()
# Create your views here.
##########################################################################
#########                     Product Views                   #########
##########################################################################


class ProductListView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, ListView
):
    model = Product
    template_name = "product/product_list.html"
    paginate_by = 5
    waffle_flag = "detail_product"
    context_object_name = "product_list"

    def get_queryset(self):
        org_product_qs = Product.objects.filter(
            organisation=self.request.user.userorganization.id
        ).order_by("-dateTimeModified")
        return org_product_qs


Product_list_view = ProductListView.as_view()


class ProductRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse(
            "product:list",
        )


Product_redirect_view = ProductRedirectView.as_view()


class ProductCreateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, CreateView
):
    model = Product
    form_class = ProductModelForm
    template_name = "product/product_create.html"
    waffle_flag = "create_product"
    context_object_name = "product"
    success_url = reverse_lazy("leads:redirectproduct")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["user_org"] = self.request.user.userorganization
        return kwargs

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "create_product"):
            product = form.save(commit=False)
            product.created_by = self.request.user
            product.organisation = self.request.user.userorganization
            if not product.name:
                messages.error(self.request, "Product name is required")
                return super(ProductCreateView, self).form_valid(form)

            else:
                try:
                    product.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Product Create error")
                    raise Http404(
                        "There was an error creating your product. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Congratulations!! Product has been added successfully.",
                    )
                    return redirect(reverse("product:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(ProductCreateView, self).form_valid(form)


Product_create_view = ProductCreateView.as_view()


class ProductUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, UpdateView
):
    model = Product
    form_class = ProductModelForm
    template_name = "product/product_update.html"
    waffle_flag = "update_product"
    context_object_name = "product"
    success_url = reverse_lazy("product:redirect")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["user_org"] = self.request.user.userorganization
        return kwargs

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "update_product"):
            product = form.save(commit=False)
            product.created_by = self.request.user
            if not product.name:
                messages.error(self.request, "Product name is required")
                return super(ProductUpdateView, self).form_valid(form)

            else:
                try:
                    product.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Product Update error")
                    raise Http404(
                        "There was an error creating your product. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Product has been updated successfully.",
                    )
                    return redirect(reverse("product:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(ProductUpdateView, self).form_valid(form)


Product_update_view = ProductUpdateView.as_view()


class ProductDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, DeleteView
):
    model = Product
    template_name = "product/product_confirm_delete.html"
    waffle_flag = "delete_product"
    context_object_name = "product"
    success_url = reverse_lazy("product:redirect")
    success_message = _("Product has been deleted.")

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.warning(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


Product_delete_view = ProductDeleteView.as_view()
