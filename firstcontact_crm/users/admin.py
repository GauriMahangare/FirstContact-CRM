from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from firstcontact_crm.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email","title","first_name","last_name","userorganization","phone_number","mobile_number",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_admin",
                    "is_team_manager",
                    "is_team_member",
                    "is_organisation_default",
                    "is_profile_complete",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username","name", "userorganization","last_login","date_joined"]
    list_filter = ('userorganization',)
    search_fields = ["name","email",]
    date_hierarchy = 'date_joined'
