
from django.views import generic
from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import logging
import waffle
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import RedirectView
from .models import Organisation
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import RedirectView, UpdateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from waffle.decorators import waffle_flag, flag_is_active
from waffle.mixins import WaffleFlagMixin
from django.http import Http404
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from invitations.utils import get_invitation_model
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

# Create your views here.
logger = logging.getLogger(__name__)
User = get_user_model()
Invitation = get_invitation_model()


class OrganisationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "organisation/organisation_create_update.html"
    model = Organisation
    fields = ["work_org_name", "work_address_line1", "work_address_line2",
              "work_address_line3", "work_address_line4", "work_address_postcode", ]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user.userorganization


Organisation_update_view = OrganisationUpdateView.as_view()

# class OrganisationCreateView(LoginRequiredMixin, WaffleFlagMixin,SuccessMessageMixin, generic.CreateView):


class OrganisationCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = "organisation/organisation_create_update.html"
    model = Organisation
    fields = ["work_org_name", "work_address_line1", "work_address_line2",
              "work_address_line3", "work_address_line4", "work_address_postcode", ]
    # success_message = _("Congratulations!!Organisation has been set; Now create your team and you are all set")
    #waffle_flag = "Create Organsation"

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user.userorganization

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, 'create_organisation'):
            organisation = form.save(commit=False)
            organisation.created_by = self.request.user
            if not organisation.work_org_name:
                messages.error(self.request, "Work Organisation name is required")
                return super(OrganisationCreateView, self).form_valid(form)
            elif not organisation.work_address_line1:
                messages.error(self.request, "First line of address is required")
                return super(OrganisationCreateView, self).form_valid(form)
            elif not organisation.work_address_postcode:
                messages.error(self.request, "Postcode is required")
                return super(OrganisationCreateView, self).form_valid(form)
            else:
                try:
                    organisation.save()
                except Exception as e:
                    print(str(e))
                    logger.critical('Organisation Create error')
                    raise Http404(
                        "There was an error creating your Organisation. If the error persists, please try again after sometime.")
                # Update user data so that org cannot be created any more by this user
                user = User.objects.get(pk=self.request.user.pk)
                user.is_organisation_default = False
                user.userorganization_id = organisation.pk
                try:
                    user.save()
                except Exception as e:
                    print(str(e))
                    logger.critical('Error updating user with organisation')
                    raise Http404(
                        "There was an error creating your Organisation. If the error persists, please try again after sometime.")
                # User.objects.update(is_organisation_default=False, userorganization_id=organisation.pk)
                messages.success(
                    self.request, "Congratulations!! Organisation set up is complete; Now invite your team members to collaborate.. Happy working!")
                return redirect('/organisation/~redirect/')
        else:
            messages.error(self.request, "Please update your subscription to continue using this feature.")
            return super(OrganisationCreateView, self).form_valid(form)


Organisation_create_view = OrganisationCreateView.as_view()


class OrganisationRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


Organisation_redirect_view = OrganisationRedirectView.as_view()


class OrganisationUserListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Invitation
    template_name = 'organisation/user_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs: Any):
        user_qs = Invitation.objects.filter(inviter_id=self.request.user.pk).order_by('-sent')
        # for u in user_qs:
        #     print(u.email)
        context = super().get_context_data(**kwargs)
        paginator = Paginator(user_qs, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            user_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            user_list = paginator.page(paginator.num_pages)
        context['user_list'] = user_list
        context['page_list'] = paginator.page_range
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)


Organisation_userList_view = OrganisationUserListView.as_view()


class OrganisationUserReinviteView(LoginRequiredMixin, SuccessMessageMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            user = Invitation.objects.get(pk=pk)
        except Exception as e:
            print(str(e))
            logger.info('Error deleting user invitation:User invitation does not exist.')
            messages.error(request, 'The user you are trying to invite has been already removed.')
            return redirect('/organisation/~userlist/')
        if not user.accepted:
            email = user.email
            try:
                user.delete()
            except Exception as e:
                print(str(e))
                messages.error(request, 'There was an error in reinviting the user. Please try after sometime')
                logger.critical('Error deleting user invitation:System error')
                return redirect('/organisation/~userlist/')
            logger.info('Invitation Deleted')
            invite = Invitation.create(email, inviter=request.user)
            invite.send_invitation(request)
            logger.info('Invitation Sent')
            messages.success(request, 'User has been reinvited')
            return redirect('/organisation/~userlist/')


Organisation_userReinvite_view = OrganisationUserReinviteView.as_view()


class OrganisationUserdeleteView(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            user = Invitation.objects.get(pk=pk)
        except Exception as e:
            print(str(e))
            logger.critical('Error deleting user.User does not exist.')
            messages.error(request, 'The user you are trying to delete has been removed already.')
            return redirect('/organisation/~userlist/')
        context = {"usermember": user}
        return render(request, 'organisation/user_confirm_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        try:
            user = Invitation.objects.get(pk=pk)
        except Exception as e:
            print(str(e))
            logger.critical('Error deleting user.User does not exist.')
            messages.error(request, 'The user you are trying to delete has been removed already.')
            return redirect('/organisation/~userlist/')
        email = user.email
        accepted = user.accepted
        try:
            user.delete()
        except Exception as e:
            print(str(e))
            messages.error(request, 'There was an error deleting the user. Please try after sometime')
            logger.critical('Error deleting user.System error')
            return redirect('/organisation/~userlist/')
        logger.info('Invited user deleted')
        if accepted:
            try:
                user = User.objects.get(email__exact=email)
            except Exception as e:
                print(str(e))
                logger.critical('Error deleting registered user.User does not exist.')
                messages.error(request, 'The user you are trying to delete has been removed already.')
                return redirect('/organisation/~userlist/')
            try:
                user.delete()
            except Exception as e:
                print(str(e))
                messages.error(request, 'There was an error deleting the user. Please try after sometime')
                logger.critical('Error deleting registered user.System error')
                return redirect('/organisation/~userlist/')
            logger.info('Registered user deleted')
            messages.success(request, 'User has been deleted.')
            return redirect('/organisation/~userlist/')
        else:
            messages.success(request, 'User has been deleted.')
            return redirect('/organisation/~userlist/')


Organisation_userdelete_view = OrganisationUserdeleteView.as_view()


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
