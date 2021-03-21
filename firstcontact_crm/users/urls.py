from django.urls import path

from firstcontact_crm.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_subscription_view,
    user_subscription_cancel_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:username>/subscription/", view=user_subscription_view, name="subscription"),
    path("<str:username>/subscription/cancel/", user_subscription_cancel_view, name="cancel-subscription"),
]
