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

from .models import Category

logger = logging.getLogger(__name__)
User = get_user_model()
# Create your views here.
##########################################################################
#########                     Categories Views                   #########
##########################################################################


class CategoryListView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, ListView
):
    model = Category
    template_name = "Category/category_list.html"
    paginate_by = 5
    waffle_flag = "detail_category"
    context_object_name = "category_list"

    def get_queryset(self):
        org_categories_qs = Category.objects.filter(
            organisation=self.request.user.userorganization.id
        ).order_by("-dateTimeModified")
        return org_categories_qs


Category_list_view = CategoryListView.as_view()


class CategoryRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse(
            "category:list",
        )


Category_redirect_view = CategoryRedirectView.as_view()


class CategoryCreateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, CreateView
):
    model = Category
    fields = ["status", "description"]
    template_name = "Category/category_create.html"
    waffle_flag = "create_category"
    context_object_name = "category"
    success_url = reverse_lazy("leads:redirectcategory")

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "create_category"):
            category = form.save(commit=False)
            category.created_by = self.request.user
            category.organisation = self.request.user.userorganization
            if not category.status:
                messages.error(self.request, "Category name is required")
                return super(CategoryCreateView, self).form_valid(form)

            else:
                try:
                    category.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Category Create error")
                    raise Http404(
                        "There was an error creating your category. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Congratulations!! Category has been added successfully.",
                    )
                    return redirect(reverse("category:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(CategoryCreateView, self).form_valid(form)


Category_create_view = CategoryCreateView.as_view()


class CategoryUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, UpdateView
):
    model = Category
    fields = ["status", "description"]
    template_name = "Category/category_update.html"
    waffle_flag = "update_category"
    context_object_name = "category"
    success_url = reverse_lazy("leads:redirectcategory")

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "update_category"):
            category = form.save(commit=False)
            category.created_by = self.request.user
            if not category.status:
                messages.error(self.request, "Category name is required")
                return super(CategoryUpdateView, self).form_valid(form)

            else:
                try:
                    category.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Category Update error")
                    raise Http404(
                        "There was an error creating your category. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Congratulations!! Category has been updated successfully.",
                    )
                    return redirect(reverse("category:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(CategoryUpdateView, self).form_valid(form)


Category_update_view = CategoryUpdateView.as_view()


class CategoryDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, DeleteView
):
    model = Category
    template_name = "Category/category_confirm_delete.html"
    waffle_flag = "delete_category"
    context_object_name = "category"
    success_url = reverse_lazy("leads:redirectcategory")
    success_message = _("Category has been deleted.")

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.warning(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


Category_delete_view = CategoryDeleteView.as_view()
