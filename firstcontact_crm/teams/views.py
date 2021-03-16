from .forms import MembershipForm
from typing import Any, Optional, Type
from django.db import models
from django.forms import forms
from django.forms.models import BaseModelForm
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
import logging
import waffle
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import RedirectView
from .models import Team, TeamMembership
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView,RedirectView
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
# from .forms import TeamMembershipForm

# Create your views here.
logger = logging.getLogger(__name__)
User = get_user_model()

# Create your views here.

def get_teams(user):
    teams_qs = Team.objects.filter(organisation=user.userorganization)
    if teams_qs.exists():
        return teams_qs
    return None

class SearchView(LoginRequiredMixin,SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        queryset = Team.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset
        }
        return render(request, 'search_results.html', context)

Team_search_view = SearchView.as_view()

class TeamListView(LoginRequiredMixin,SuccessMessageMixin,ListView):
    model = Team
    template_name = 'teams/team_list.html'
    paginate_by = 5
    

    def get_context_data(self, **kwargs: Any):
        team_qs = Team.objects.filter(organisation=self.request.user.userorganization).order_by('-dateTimeModified')
        context = super().get_context_data(**kwargs)
        paginator = Paginator(team_qs, self.paginate_by)
        page = self.request.GET.get('page')

        
        try:
            team_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            team_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            team_list = paginator.page(paginator.num_pages)
        context['team_list'] = team_list
        context['page_list'] = paginator.page_range
        return context


    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
        
    
Team_list_view = TeamListView.as_view()

class TeamUpdateView(LoginRequiredMixin, SuccessMessageMixin,UpdateView):
    template_name = "teams/team_update.html"
    model = Team
    fields = ["name","description",]
    success_message = _("Information successfully updated.")
    waffle_flag = 'create_team'
    slug_field = 'slug'  # The name of the field on the model that contains the slug
    slug_url_kwarg = 'slug_text' # The name of the URLConf keyword argument that contains the slug
 
    def get_context_data(self, **kwargs):
        kwargs['team'] = self.get_object()
        return super().get_context_data(**kwargs)
    
    # def get_queryset(self):
    #     slug_text = self.kwargs['slug_text']
    #     qs=Team.objects.filter(slug=slug_text)
    #     if qs.exists():
    #         return qs.first()
    #     else:
    #         return HttpResponse("<h1> Page not found. </h1>")

    # def get_object(self, queryset: Optional[models.query.QuerySet]) -> models.Model:
    #     return super().get_object(queryset=queryset)
    
    def form_valid(self, form):
        if waffle.flag_is_active(self.request, 'create_team'):
            team = form.save(commit=False)
            team.created_by = self.request.user
            if  not team.name:
                messages.error(self.request, "Team name is required")
                return super(TeamUpdateView, self).form_valid(form)
            
            else:
                try:
                    team.save()
                except:
                    logger.critical('Team Update error')
                    raise Http404 ("There was an error updating your Team. If the error persists, please try again after sometime.")
                messages.success(self.request, "Information has been updated.")
                return redirect('/teams/~redirect/')
            #     return redirect(reverse("team-list", kwargs={
            #     'pk': form.instance.pk
            # }))
        else:
            messages.error(self.request, "Please update your subscription to continue using this feature.")
            return super(TeamUpdateView, self).form_valid(form)

Team_update_view = TeamUpdateView.as_view()


class TeamDetailView(LoginRequiredMixin,SuccessMessageMixin,WaffleFlagMixin,DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'
    waffle_flag = 'create_team'
    slug_field = 'slug'  # The name of the field on the model that contains the slug
    slug_url_kwarg = 'slug_text' # The name of the URLConf keyword argument that contains the slug

    
Team_detail_view = TeamDetailView.as_view()
    
class TeamCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Team
    fields = ["name","description",]
    template_name = 'teams/team_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if waffle.flag_is_active(self.request, 'create_team'):
            team = form.save(commit=False)
            team.created_by = self.request.user
            team.organisation = self.request.user.userorganization
            if  not team.name:
                messages.error(self.request, "Team name is required")
                return super(TeamCreateView, self).form_valid(form)
            
            else:
                try:
                    team.save()
                except:
                    logger.critical('Team Create error')
                    raise Http404 ("There was an error creating your Team. If the error persists, please try again after sometime.")
                # Update user data so that org cannot be created any more by this user
            
                messages.success(self.request, "Congratulations!! Team has been set; Now assign team members to this team")
                return redirect('/teams/~redirect/')
        else:
            messages.error(self.request, "Please update your subscription to continue using this feature.")
            return super(TeamCreateView, self).form_valid(form)    

Team_create_view = TeamCreateView.as_view()

class TeamRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("teams:list",)

Team_redirect_view = TeamRedirectView.as_view()

class TeamDeleteView(LoginRequiredMixin,SuccessMessageMixin,WaffleFlagMixin,DeleteView):
    model = Team
    success_url = '/teams/~redirect/'
    template_name = 'teams/team_confirm_delete.html'
    success_message = _("Team has been deleted.")
    context_object_name = 'team'
    warning_message = _("Team has been deleted.")
    waffle_flag = "create_team"
    slug_field = 'slug'  # The name of the field on the model that contains the slug
    slug_url_kwarg = 'slug_text' # The name of the URLConf keyword argument that contains the slug


Team_delete_view = TeamDeleteView.as_view()

class TeamMembersView(LoginRequiredMixin,SuccessMessageMixin,WaffleFlagMixin,ListView):
    model = TeamMembership
    waffle_flag = 'create_team'
    template_name = 'teams/team_members_list.html'
    paginate_by = 5
    slug_field = 'slug'  # The name of the field on the model that contains the slug
    slug_url_kwarg = 'slug_text' # The name of the URLConf keyword argument that contains the slug
    
        
    def get_context_data(self, **kwargs: Any):
        slug_text = self.kwargs['slug_text']
        print(slug_text)
        qs=Team.objects.filter(slug=slug_text)
        if qs.exists():
            print("Team found")
            team= qs.first()
            print(team)
            print(team.pk)
            print(team.name)
        else:
            return HttpResponse("<h1> Page not found. </h1>")
        team_qs = TeamMembership.objects.filter(team=team.pk).order_by('-dateTimeModified')
        context = super().get_context_data(**kwargs)
        paginator = Paginator(team_qs, self.paginate_by)
        page = self.request.GET.get('page')

        
        try:
            team_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            team_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            team_list = paginator.page(paginator.num_pages)
        context['team_list'] = team_list
        context['page_list'] = paginator.page_range
        context['team_name'] = team.name
        context['slug_text'] = slug_text
        return context


    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

Team_members_view = TeamMembersView.as_view()


class TeamMemberDeleteView(LoginRequiredMixin,SuccessMessageMixin,WaffleFlagMixin,DeleteView):
    model = TeamMembership
    success_url = '/teams/~redirect/'
    template_name = 'teams/team_membership_confirm_delete.html'
    context_object_name = 'team_member'
    warning_message = _("Membership has been removed.")
    waffle_flag = "create_team"
    slug_field = 'slug'  # The name of the field on the model that contains the slug
    slug_url_kwarg = 'slug_text' # The name of the URLConf keyword argument that contains the slug


Team_members_delete_view = TeamMemberDeleteView.as_view()

# class TeammembershipCreateView(LoginRequiredMixin,SuccessMessageMixin,WaffleFlagMixin,CreateView):
#     model = User
#     fields = ["email"]
#     template_name = 'teams/team_membership_add.html'
#     waffle_flag = "create_team"
#     form_class = TeamMembershipForm
#     slug_field = 'slug'  # The name of the field on the model that contains the slug
#     slug_url_kwarg = 'slug_text' # The name of the URLConf keyword argument that contains the slug


#     def get_context_data(self, **kwargs: Any):
#         print("in context data")
#         context = super().get_context_data(**kwargs)
#         # slug_text = self.kwargs['slug_text']
#         print("*** in team membership create ***")
#         # print(slug_text)
#         try:
#             team=Team.objects.get(pk=54)
#         except:
#             return HttpResponse("<h1> Team not found. </h1>")
#         else:
#             print("Team found")
#             # team= qs.first()
#             print(team)
#             print(team.pk)
#             print(team.name)
#             context['pk'] = team.pk
#             context['team_name'] = team.name
#             return context

#     # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
#     #     return super().get(request, *args, **kwargs)

#     def form_valid(self, form):
#         if waffle.flag_is_active(self.request, 'create_team'):
#             slug_text = self.kwargs['slug_text']
#             print("*** in team membership post ***")
#             print(slug_text)
#             qs=Team.objects.filter(slug=slug_text)
#             if qs.exists():
#                 print("Team found")
#                 team= qs.first()
#                 print(team)
#                 print(team.pk)
#                 print(team.name)
#             else:
#                 return HttpResponse("<h1> Page not found. </h1>")
#             membership = TeamMembership()
#             membership.team = team.pk
#             membership.member = form.save(commit=False)
#             print(membership)
#             try:
#                 membership.save()
#             except:
#                 logger.critical('Membership create error')
#                 raise Http404 ("There was an error adding the user to the team. If the error persists, please try again after sometime.")
#                 # Update user data so that org cannot be created any more by this user
            
#             messages.success(self.request, "User has been added to the team.")
#             return redirect('/teams/~redirect/')
#         else:
#             messages.error(self.request, "Please update your subscription to continue using this feature.")
#             return super(TeamCreateView, self).form_valid(form)    

# Team_membership_add_view = TeammembershipCreateView.as_view()

def add_member_view(request,*args, **kwargs):
    user = get_object_or_404(User, id=request.user.pk)
    organisation = user.userorganization
    team_qs = Team.objects.filter(organisation = organisation )
    if team_qs.exists():
        team_defined = True
    else:
        team_defined = False
    user_qs = User.objects.filter(userorganization = organisation)
    if user_qs.exists():
        user_defined = True
    else:
        user_defined = False
    context={}
    if request.POST:
        form = MembershipForm(organisation,request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/teams/~redirect/')
    else:
        form = MembershipForm(organisation)
    
    context={   "form":form,
                "user_defined" : user_defined,
                "team_defined" : team_defined
            }
    
    return render(request,'teams/team_membership_add.html', context)