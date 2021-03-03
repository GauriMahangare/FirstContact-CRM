
from django.urls import path

from teams.views import (
    Team_redirect_view,
    Team_update_view,
    Team_create_view,
    Team_delete_view,
    Team_list_view,
    Team_search_view,
    Team_detail_view,
)

app_name = "teams"
urlpatterns = [
    path("~update/<int:pk>/", view=Team_update_view, name="update"),
    path("~create/", view=Team_create_view, name="create"),
    path("~delete/<int:pk>", view=Team_delete_view, name="delete"),
    path("~list/", view=Team_list_view, name="list"),
    path("~search/", view=Team_search_view, name="search"),
    path("~detail/", view=Team_detail_view, name="detail"),
    path("~redirect/", view=Team_redirect_view, name="redirect"),
]