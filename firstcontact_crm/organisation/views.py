
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import logging
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import RedirectView
from .models import Organisation
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import RedirectView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your views here.
logger = logging.getLogger(__name__)
User = get_user_model()
class OrganisationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "organisation/organisation_create_update.html"
    model = Organisation
    fields = ["work_org_name","work_address_line1","work_address_line2","work_address_line3","work_address_line4","work_address_postcode",]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user.userorganization

Organisation_update_view = OrganisationUpdateView.as_view()

class OrganisationCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    print("in create org view")
    template_name = "organisation/organisation_create_update.html"
    model = Organisation
    fields = ["work_org_name","work_address_line1","work_address_line2","work_address_line3","work_address_line4","work_address_postcode",]
    # success_message = _("Organisation has been set; Now create your team and you are all set")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user.userorganization

    def form_valid(self, form):
        organisation = form.save(commit=False)
        organisation.created_by = self.request.user
        if  not organisation.work_org_name:
            messages.error(self.request, "Work Organisation name is required")
            return super(OrganisationCreateView, self).form_valid(form)
        elif not organisation.work_address_line1:
            messages.error(self.request, "First line of address is required")
            return super(OrganisationCreateView, self).form_valid(form)
        elif not organisation.work_address_postcode:
            messages.error(self.request, "Postcode is required")
            return super(OrganisationCreateView, self).form_valid(form)
        else:
            organisation.save()
            # Update user data so that org cannot be created any more by this user
            User.objects.update(is_organisation_default=False, userorganization_id=organisation.pk)
            messages.success(self.request, "Organisation has been set; Now create your team and you are all set")
            return redirect('/organisation/~redirect/')

Organisation_create_view = OrganisationCreateView.as_view()

class OrganisationRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

Organisation_redirect_view = OrganisationRedirectView.as_view()




















# @login_required()
# def organisation_create_view(request, *args, **kwargs):
#     form = OrganisationModelForm(request.POST or None)
#     if (form.is_valid()):
#         obj = form.save(commit=False)
#         # add required validations if required
#         obj.user = request.user
#         obj.save()
#         form = OrganisationModelForm() # cleaned form returned
#         return HttpResponseRedirect("~redirect/")
#     context={"form":form}
#     return render(request,"organisation_create_update.html",context)

# @login_required()
# def organisation_update_view(request, *args, **kwargs):
#     context ={}
#     try:
#        obj = Organisation.objects.get(pk=pk)
#     except Organisation.DoesNotExist:
#         raise Http404
#     form = OrganisationModelForm(request.POST or None , instance = obj)
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = request.user
#         form = OrganisationModelForm(request.POST or None , instance = obj)
#         form.save()
#         #return HttpResponseRedirect("backtest/<int:pk>/")
#         form = OrganisationModelForm()
#         return redirect('user_detail_view')
#     context={ "form":form }
#     return render(request, "organisation_create_update.html", context)
