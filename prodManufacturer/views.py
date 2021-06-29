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

from .models import Manufacturer

logger = logging.getLogger(__name__)
User = get_user_model()
# Create your views here.
##########################################################################
#########                     Categories Views                   #########
##########################################################################


class ManufacturerListView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, ListView
):
    model = Manufacturer
    template_name = "manufacturer/manufacturer_list.html"
    paginate_by = 5
    waffle_flag = "detail_manufacturer"
    context_object_name = "manufacturer_list"

    def get_queryset(self):
        org_categories_qs = Manufacturer.objects.filter(
            organisation=self.request.user.userorganization.id
        ).order_by("-dateTimeModified")
        return org_categories_qs


Manufacturer_list_view = ManufacturerListView.as_view()


class ManufacturerRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse(
            "manufacturer:list",
        )


Manufacturer_redirect_view = ManufacturerRedirectView.as_view()


class ManufacturerCreateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, CreateView
):
    model = Manufacturer
    fields = ["name", "address", "is_active"]
    template_name = "manufacturer/manufacturer_create.html"
    waffle_flag = "create_manufacturer"
    context_object_name = "manufacturer"
    success_url = reverse_lazy("manufacturer:list")

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "create_manufacturer"):
            manufacturer = form.save(commit=False)
            manufacturer.created_by = self.request.user
            manufacturer.organisation = self.request.user.userorganization
            if not manufacturer.name:
                messages.error(self.request, "Manufacturer name is required")
                return super(ManufacturerCreateView, self).form_valid(form)

            else:
                try:
                    manufacturer.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Manufacturer Create error")
                    raise Http404(
                        "There was an error creating your manufacturer. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Manufacturery has been added successfully.",
                    )
                    return redirect(reverse("manufacturer:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(ManufacturerCreateView, self).form_valid(form)


Manufacturer_create_view = ManufacturerCreateView.as_view()


class ManufacturerUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, UpdateView
):
    model = Manufacturer
    fields = ["name", "address", "is_active"]
    template_name = "manufacturer/manufacturer_update.html"
    waffle_flag = "update_manufacturer"
    context_object_name = "manufacturer"
    success_url = reverse_lazy("manufacturer:list")

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, "update_manufacturer"):
            manufacturer = form.save(commit=False)
            manufacturer.created_by = self.request.user
            if not manufacturer.name:
                messages.error(self.request, "Manufacturer name is required")
                return super(ManufacturerUpdateView, self).form_valid(form)

            else:
                try:
                    manufacturer.save()
                except Exception as e:
                    print(str(e))
                    logger.critical("Manufacturer Update error")
                    raise Http404(
                        "There was an error creating your manufacturer. If the error persists, please try again after sometime."
                    )
                else:
                    messages.success(
                        self.request,
                        "Manufacturer has been updated successfully.",
                    )
                    return redirect(reverse("manufacturer:list"))
        else:
            messages.error(
                self.request,
                "Please update your subscription to continue using this feature.",
            )
            return super(ManufacturerUpdateView, self).form_valid(form)


Manufacturer_update_view = ManufacturerUpdateView.as_view()


class ManufacturerDeleteView(
    LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, DeleteView
):
    model = Manufacturer
    template_name = "manufacturer/manufacturer_confirm_delete.html"
    waffle_flag = "delete_manufacturer"
    context_object_name = "manufacturer"
    success_url = reverse_lazy("manufacturer:list")
    success_message = _("Manufacturer has been deleted.")

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.warning(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


Manufacturer_delete_view = ManufacturerDeleteView.as_view()
