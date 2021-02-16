from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):

    error_messages = admin_forms.UserCreationForm.error_messages.update(
        {
            "username": {"unique": _("This username has already been taken.")},
            "userorganization": {"unique": _("This organisation has already been registered.Please contact your adminstrator for access")}
        })

    userorganization = forms.CharField(max_length=150, min_length=4, required=True, help_text='Required: Organisation Name',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work Organisation Name'}))
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("username","userorganization",)
        field_classes = {'username': admin_forms.UsernameField}

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])

    def clean_userorganization(self):
        userorganization = self.cleaned_data["userorganization"]

        try:
            User.objects.get(userorganization=userorganization)
        except User.DoesNotExist:
            return userorganization

        raise ValidationError(self.error_messages["duplicate_userorganization"])