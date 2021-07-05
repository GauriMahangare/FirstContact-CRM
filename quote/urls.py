from django.urls import path

from quote.views import (
    ####### Quote view ##########
    Quote_create_view,
    Quote_update_view,
    Quote_delete_view,
    Quote_list_view,
    Quote_redirect_view,
)

app_name = "quote"
urlpatterns = [
    ################# Categories URLS #################
    path(
        "~create/>",
        view=Quote_create_view,
        name="create",
    ),
    path(
        "~update/<int:pk>",
        view=Quote_update_view,
        name="update",
    ),
    path(
        "~delete/<int:pk>",
        view=Quote_delete_view,
        name="delete",
    ),
    path("~list/", view=Quote_list_view, name="list"),
    path("~redirect/", view=Quote_redirect_view, name="redirect"),
]
