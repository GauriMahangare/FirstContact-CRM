from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

from organisation.models import Organisation

User = get_user_model()
class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):

    error_messages = admin_forms.UserCreationForm.error_messages.update(
        {
            "username": {"unique": _("This username has already been taken.")},
        })

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("username",)
        field_classes = {'username': admin_forms.UsernameField}

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])



# class RegisterForm(forms.Form):
#     error_messages = forms.Form.error_messages.update(
#         {
#             "username": {"unique": _("This username has already been taken.")},
#             "userorganization": {"unique": _("This organisation has already been registered.Please contact your adminstrator for access")},
#             'password_mismatch': _('The two password fields didn’t match.'),
#             'email_inuse': _('This email is already in use.')
#         })
#     first_name = forms.CharField(
#                     max_length=12,
#                     min_length=4,
#                     required=True,
#                     help_text='Required: First Name',
#                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
#     )
#     last_name = forms.CharField(
#                     max_length=12,
#                     min_length=4,
#                     required=True,
#                     help_text='Required: Last Name',
#                     widget=(forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}))
#     )
#     userorganization = forms.CharField(
#                     max_length=150,
#                     min_length=4,
#                     required=True,
#                     help_text='Required: Organisation Name',
#                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work Organisation Name'})
#     )
#     email = forms.EmailField(
#                     max_length=60,
#                     help_text='Required. Provide a valid email address.',
#                     widget=(forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email Address'}))
#     )
#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         strip=False,
#         help_text=_("Enter the same password as before, for verification."),
#     )
#     # username = forms.CharField(
#     #     label=_('Username'),
#     #     max_length=150,
#     #     help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#     #     validators=[username_validator],
#     #     error_messages={'unique': _("A user with that username already exists.")},
#     #     widget=forms.TextInput(attrs={'class': 'form-control'})
#     # )

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)

#         # def __init__(self, *args, **kwargs):

#         # if self._meta.model.email in self.fields:
#         #     self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2

#     def _post_clean(self):
#         super()._post_clean()
#         # Validate the password after self.instance is updated with form data
#         # by super().
#         password = self.cleaned_data.get('password2')
#         if password:
#             try:
#                 password_validation.validate_password(password, self.instance)
#             except forms.ValidationError as error:
#                 self.add_error('password2', error)

#     def clean_userorganization(self):
#         userorganization = self.cleaned_data["userorganization"]

#         try:
#             Organisation.objects.filter(userorganization__iexact=userorganization)
#         except User.DoesNotExist:
#             return userorganization

#         raise ValidationError(self.error_messages["userorganization_alreadyregistered"])

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         qs = User.objects.filter(email__iexact=email)
#         if qs.exists():
#             raise forms.ValidationError(self.error_messages['email_inuse'],code='email_inuse')
#         return email


#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

