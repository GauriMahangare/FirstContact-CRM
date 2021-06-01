
from datetime import date, datetime, timedelta

from leads.forms import LeadModelForm
from django import forms
from typing import Any, Optional, Type
import logging
from django.contrib.auth.decorators import login_required
from django.db import models
from django.forms import forms
from django.forms.models import BaseModelForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render

import waffle
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# from waffle.decorators import waffle_flag,flag_is_active
from waffle.mixins import WaffleFlagMixin
from django.http import Http404
from organisation.models import Organisation
from .models import Category, Lead
# from .forms import LeadMembershipForm

# Create your views here.
logger = logging.getLogger(__name__)
User = get_user_model()


def get_leads(user):
    leads_qs = Lead.objects.filter(organisation=user.userorganization).order_by('-dateTimeModified')
    if leads_qs.exists():
        return leads_qs
    return None


class SearchView(LoginRequiredMixin, SuccessMessageMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = Lead.objects.filter(organisation=self.request.user.userorganization).order_by('-dateTimeModified')
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(user=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset,
            'categories': Category.objects.all()
        }
        return render(request, 'search_results.html', context)


Lead_search_view = SearchView.as_view()


def is_valid_queryparam(param):
    return param != '' and param is not None


def input_filter(request):
    print(request)
    qs = Lead.objects.filter(organisation=request.user.userorganization).order_by('-dateTimeModified')
    categories = Category.objects.all()
    assigned_to_team_query = request.GET.get('assigned_to_team')
    source_exact_query = request.GET.get('source_exact')
    work_organisation_query = request.GET.get('work_organisation')
    lead_rating_query = request.GET.get('lead_rating')
    close_reason_query = request.GET.get('close_reason')

    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    date_min = request.GET.get('add_date_min')
    date_max = request.GET.get('add_date_max')
    category = request.GET.get('category')
    reviewed = request.GET.get('reviewed')
    not_reviewed = request.GET.get('notReviewed')

    if is_valid_queryparam(assigned_to_team_query):
        qs = qs.filter(team__icontains=assigned_to_team_query)

    elif is_valid_queryparam(source_exact_query):
        qs = qs.filter(source=source_exact_query)

    elif is_valid_queryparam(work_organisation_query):
        qs = qs.filter(Q(work_org_name__icontains=work_organisation_query)
                       ).distinct()
    elif is_valid_queryparam(lead_rating_query):
        qs = qs.filter(Q(lead_Ratings__icontains=lead_rating_query)
                       ).distinct()
    elif is_valid_queryparam(close_reason_query):
        qs = qs.filter(Q(closeReason__icontains=close_reason_query)
                       ).distinct()

    if is_valid_queryparam(view_count_min):
        qs = qs.filter(views__gte=view_count_min)

    if is_valid_queryparam(view_count_max):
        qs = qs.filter(views__lt=view_count_max)

    if is_valid_queryparam(date_min):
        qs = qs.filter(dateTimeCreated__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(dateTimeCreated__lt=date_max)

    if is_valid_queryparam(category) and category != 'Choose...':
        qs = qs.filter(status__id=category)

    if reviewed == 'on':
        now = datetime.now()
        seven_days_ago = now - timedelta(weeks=1)
        qs = qs.filter(dateTimeModified__gte=seven_days_ago)

    elif not_reviewed == 'on':
        now = datetime.now()
        seven_days_ago = now - timedelta(weeks=1)
        qs = qs.filter(dateTimeModified__lt=seven_days_ago)

    return qs


def infinite_filter(request):
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    return Lead.objects.all()[int(offset): int(offset) + int(limit)]


def is_there_more_data(request):
    offset = request.GET.get('offset')
    if int(offset) > Lead.objects.all().count():
        return False
    return True


class LeadListView(LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, ListView):
    model = Lead
    template_name = 'leads/lead_list.html'
    paginate_by = 25
    # context_object_name = 'lead'
    waffle_flag = 'detail_lead'

    def get_context_data(self, **kwargs: Any):
        lead_qs = input_filter(self.request)
        context = super().get_context_data(**kwargs)
        paginator = Paginator(lead_qs, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            lead_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            lead_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            lead_list = paginator.page(paginator.num_pages)
        context['lead_list'] = lead_list
        context['page_list'] = paginator.page_range
        context['categories'] = Category.objects.all()
        return context


Lead_list_view = LeadListView.as_view()


class LeadUpdateView(LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, UpdateView):
    template_name = "leads/lead_update.html"
    model = Lead
    form_class = LeadModelForm
    success_message = _("Information successfully updated.")
    waffle_flag = 'update_lead'

    def get_success_url(self):
        return reverse("leads:list")


Lead_update_view = LeadUpdateView.as_view()


class LeadDetailView(LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, DetailView):
    model = Lead
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'
    waffle_flag = 'detail_lead'
    # slug_field = 'slug'  # The name of the field on the model that contains the slug
    # slug_url_kwarg = 'slug_text'  # The name of the URLConf keyword argument that contains the slug


Lead_detail_view = LeadDetailView.as_view()


class LeadCreateView(LoginRequiredMixin, SuccessMessageMixin, WaffleFlagMixin, CreateView):
    model = Lead
    form_class = LeadModelForm
    template_name = 'leads/lead_create.html'
    success_message = _("Lead added successfully.")
    waffle_flag = 'create_lead'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, 'create_team'):
            lead = form.save(commit=False)
            lead.created_by = self.request.user
            if not lead.assigned_to:
                lead.assigned_to = self.request.user
            lead.organisation = self.request.user.userorganization
            if not lead.email:
                messages.error(self.request, "lead email is required")
                return super(LeadCreateView, self).form_valid(form)

            else:
                try:
                    lead.save()
                except Exception as e:
                    print(str(e))
                    logger.critical('lead Create error')
                    raise Http404(
                        "There was an error creating your lead. If the error persists, please try again after sometime.")
                # Update user data so that org cannot be created any more by this user
                else:
                    messages.success(
                        self.request, "Congratulations!! lead has been added; Now assign a members to this lead")
                    return redirect("leads:redirect")
        else:
            messages.error(self.request, "Please update your subscription to continue using this feature.")
            return super(LeadCreateView, self).form_valid(form)


Lead_create_view = LeadCreateView.as_view()


class LeadRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("leads:list",)


Lead_redirect_view = LeadRedirectView.as_view()


# Create your views here.

# Function view to manage multiple deletes.
@ login_required()
def multi_lead_delete_view(request, *args, **kwargs):
    context = {}
    leads_tobe_deleted = ''
    leads_tobe_deleted_list = []
    leads_tobe_deleted_email_list = []
    # leads_tobe_deleted = request.GET.get('selectedRowsLeadId', None)
    leads_tobe_deleted = request.META['QUERY_STRING']
    leads_tobe_deleted_list = leads_tobe_deleted.split(",")

    for lead in leads_tobe_deleted_list:
        try:
            obj = Lead.objects.get(pk=lead)
        except Exception as e:
            print(str(e))
            logger.critical('GET:There was an error deleting your lead  %s', lead, exc_info=1)
            raise Http404("There was an error deleting your lead. If the error persists, please try again after sometime.")
        else:
            if request.method == 'POST':
                try:
                    obj.delete()
                except Exception as e:
                    print(str(e))
                    logger.critical('POST:There was an error deleting your lead  %s', lead, exc_info=1)
                    raise Http404(
                        "There was an error deleting your lead. If the error persists, please try again after sometime.")
                else:
                    logger.info('Lead deleted successfully  %s', lead, exc_info=1)
                    return redirect("leads:redirect")

            leads_tobe_deleted_email_list.append(obj.email)
            print(obj.email)

    context['leads_tobe_deleted'] = leads_tobe_deleted_list
    context['leads_tobe_deleted_email'] = leads_tobe_deleted_email_list
    context['leads_tobe_deleted_count'] = len(leads_tobe_deleted_list)
    return render(request, "leads/lead_confirm_delete.html", context)
