from django.urls import path

from category.views import (
    ####### Category view ##########
    Category_create_view,
    Category_update_view,
    Category_delete_view,
    Category_list_view,
    Category_redirect_view,
)

app_name = "category"
urlpatterns = [
    ################# Categories URLS #################
    path(
        "~create/>",
        view=Category_create_view,
        name="create",
    ),
    path(
        "~update/<int:pk>",
        view=Category_update_view,
        name="update",
    ),
    path(
        "~delete/<int:pk>",
        view=Category_delete_view,
        name="delete",
    ),
    path("~list/", view=Category_list_view, name="list"),
    path("~redirect/", view=Category_redirect_view, name="redirect"),
]
