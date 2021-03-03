from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
import logging
from django.views.generic.edit import CreateView
import waffle
from django.http import Http404
from waffle.decorators import waffle_flag,flag_is_active
from waffle.mixins import WaffleFlagMixin

User = get_user_model()
logger = logging.getLogger(__name__)

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["email","title","first_name","last_name","phone_number","mobile_number",]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user

    def form_valid(self, form: BaseForm) -> HttpResponse:
        user = form.save(commit=False)
        if  not user.first_name:
            messages.error(self.request, "First Name is required")
            return super(UserUpdateView, self).form_valid(form)
        elif not user.last_name:
            messages.error(self.request, "Last Name is required")
            return super(UserUpdateView, self).form_valid(form)
        elif not user.mobile_number:
            messages.error(self.request, "Mobile number is required")
            return super(UserUpdateView, self).form_valid(form)
        else:
            try:
                if (user.first_name and user.last_name and user.mobile_number):
                    user.is_profile_complete=True
                user.save()
            except :
                logger.critical('Error updating user profile')
                raise Http404 ("There was an error updating your profile. If the error persists, please try again after sometime.")
        return super(UserUpdateView, self).form_valid(form)

user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
