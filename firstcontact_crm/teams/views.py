from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import logging
import waffle
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import RedirectView
from .models import Team
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView,RedirectView
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# from waffle.decorators import waffle_flag,flag_is_active
# from waffle.mixins import WaffleFlagMixin
from django.http import Http404
from organisation.models import Organisation

# Create your views here.
logger = logging.getLogger(__name__)
User = get_user_model()

# Create your views here.

def get_teams(user):
    teams_qs = Team.objects.filter(organisation=user.userorganization)
    if teams_qs.exists():
        return teams_qs
    return None

class SearchView(View):
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

class TeamListView(ListView):
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
    success_message = _("Information successfully updated")

    def get_context_data(self, **kwargs):
        kwargs['team'] = self.get_object()
        return super().get_context_data(**kwargs)

    def get_object(self, queryset=None):
        return Team.objects.get(pk=self.kwargs.get("pk"))

    
    def form_valid(self, form):
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

Team_update_view = TeamUpdateView.as_view()


class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

Team_detail_view = TeamDetailView.as_view()
    
class TeamCreateView(CreateView):
    model = Team
    fields = ["name","description",]
    template_name = 'teams/team_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
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

Team_create_view = TeamCreateView.as_view()

class TeamRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("teams:list",)

Team_redirect_view = TeamRedirectView.as_view()

class TeamDeleteView(DeleteView):
    model = Team
    success_url = '/teams/~redirect/'
    template_name = 'teams/team_confirm_delete.html'
    context_object_name = 'team'
    warning_message = _("Team has been deleted.")

    # def form_valid(self, form):
    #     try:
    #         team.delete()
    #     except:
    #         logger.critical('Team Delete error')
    #         raise Http404 ("There was an error deleting your Team. If the error persists, please try again after sometime.")
    #         # Update user data so that org cannot be created any more by this user
        
    #     messages.success(self.request, "Congratulations!! Team has been set; Now assign team members to this team")
    #     return redirect('/teams/~redirect/')

Team_delete_view = TeamDeleteView.as_view()


