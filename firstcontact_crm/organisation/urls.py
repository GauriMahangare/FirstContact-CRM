
from django.urls import path

from organisation.views import (
    Organisation_redirect_view,
    Organisation_update_view,
    Organisation_create_view,
    Organisation_userList_view,
    Organisation_userReinvite_view,
    Organisation_userdelete_view,
)

app_name = "organisation"
urlpatterns = [
    path("~update/", view=Organisation_update_view, name="update"),
    path("~create/", view=Organisation_create_view, name="create"),
    path("~redirect/", view=Organisation_redirect_view, name="redirect"),
    path("~userlist/", view=Organisation_userList_view, name="list"),
    path("~userreinvite/<int:pk>", view=Organisation_userReinvite_view, name="invite"),
    path("~userredelete/<int:pk>", view=Organisation_userdelete_view, name="delete"),

]
