import logging
from typing import Any, Optional
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

from .models import ProdCategory

logger = logging.getLogger(__name__)
User = get_user_model()
# Create your views here.
##########################################################################
#########                     Categories Views                   #########
##########################################################################


class ProdCategoryListView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, ListView
):
    model = ProdCategory
    template_name = "ProdCategory/category_list.html"
    paginate_by = 5
    waffle_flag = "detail_prodcategory"
    context_object_name = "category_list"

    def get_queryset(self):
        org_categories_qs = ProdCategory.objects.filter(
            organisation=self.request.user.userorganization.id
        ).order_by("-dateTimeModified")
        return org_categories_qs


ProdCategory_list_view = ProdCategoryListView.as_view()


class ProdCategoryRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse(
            "prodCategory:list",
        )


ProdCategory_redirect_view = ProdCategoryRedirectView.as_view()


class ProdCategoryCreateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, CreateView
):
    model = ProdCategory
    fields = ["name", "description"]
    template_name = "ProdCategory/category_create.html"
    waffle_flag = "create_prodcategory"
    context_object_name = "category"
    success_url = reverse_lazy("prodCategory:list")

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "create_prodcategory"):
            category = form.save(commit=False)
            category.created_by = self.request.user
            category.organisation = self.request.user.userorganization
            if not category.name:
                messages.error(self.request, "ProdCategory name is required")
                return super(ProdCategoryCreateView, self).form_valid(form)

            else:
                try:
                    category.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("ProdCategory Create error")
                    raise Http404(
                        "There was an error creating your category. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Product Category has been added successfully.",
                    )
                    return redirect(reverse("prodCategory:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(ProdCategoryCreateView, self).form_valid(form)


ProdCategory_create_view = ProdCategoryCreateView.as_view()


class ProdCategoryUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, UpdateView
):
    model = ProdCategory
    fields = ["name", "description"]
    template_name = "ProdCategory/category_update.html"
    waffle_flag = "update_prodcategory"
    context_object_name = "category"
    success_url = reverse_lazy("prodCategory:list")

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "update_prodcategory"):
            category = form.save(commit=False)
            category.created_by = self.request.user
            if not category.name:
                messages.error(self.request, "ProdCategory name is required")
                return super(ProdCategoryUpdateView, self).form_valid(form)

            else:
                try:
                    category.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("ProdCategory Update error")
                    raise Http404(
                        "There was an error creating your category. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Product Category has been updated successfully.",
                    )
                    return redirect(reverse("prodCategory:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(ProdCategoryUpdateView, self).form_valid(form)


ProdCategory_update_view = ProdCategoryUpdateView.as_view()


class ProdCategoryDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, DeleteView
):
    model = ProdCategory
    template_name = "ProdCategory/category_confirm_delete.html"
    waffle_flag = "delete_prodcategory"
    context_object_name = "category"
    success_url = reverse_lazy("prodCategory:list")
    success_message = _("Product Category has been deleted.")

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.warning(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


ProdCategory_delete_view = ProdCategoryDeleteView.as_view()
