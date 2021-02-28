
from django.urls import path

from organisation.views import (
    Organisation_redirect_view,
    Organisation_update_view,
    Organisation_create_view,
)

app_name = "organisation"
urlpatterns = [
    path("~update/", view=Organisation_update_view, name="update"),
    path("~create/", view=Organisation_create_view, name="create"),
    path("~redirect/", view=Organisation_redirect_view, name="redirect"),
]
