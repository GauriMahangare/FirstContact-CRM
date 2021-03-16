
from django.urls import path


from teams.views import (
    Team_redirect_view,
    Team_update_view,
    Team_create_view,
    Team_delete_view,
    Team_list_view,
    Team_search_view,
    Team_detail_view,
    Team_members_view,
    Team_members_delete_view,
    add_member_view,
)

app_name = "teams"
urlpatterns = [
#    path("~update/<int:pk>/", view=Team_update_view, name="update"),
    path("~update/<slug:slug_text>", view=Team_update_view, name="update"),
    path("~create/", view=Team_create_view, name="create"),
   # path("~delete/<int:pk>", view=Team_delete_view, name="delete"),
    path("~delete/<slug:slug_text>", view=Team_delete_view, name="delete"),
    path("~list/", view=Team_list_view, name="list"),
    path("~search/", view=Team_search_view, name="search"),
    path("~detail/<slug:slug_text>", view=Team_detail_view, name="detail"),
    path("~redirect/", view=Team_redirect_view, name="redirect"),
    path("~members/<slug:slug_text>", view=Team_members_view, name="members"),
    path("~members/delete/<slug:slug_text>", view=Team_members_delete_view, name="remove_members"),
    path('~members/add/', add_member_view, name="add_members"), 
]