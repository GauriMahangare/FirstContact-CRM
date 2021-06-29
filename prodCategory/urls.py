from django.urls import path

from prodCategory.views import (
    ####### Product Category view ##########
    ProdCategory_create_view,
    ProdCategory_update_view,
    ProdCategory_delete_view,
    ProdCategory_list_view,
    ProdCategory_redirect_view,
)

app_name = "prodCategory"
urlpatterns = [
    ################# Categories URLS #################
    path(
        "~create/>",
        view=ProdCategory_create_view,
        name="create",
    ),
    path(
        "~update/<int:pk>",
        view=ProdCategory_update_view,
        name="update",
    ),
    path(
        "~delete/<int:pk>",
        view=ProdCategory_delete_view,
        name="delete",
    ),
    path("~list/", view=ProdCategory_list_view, name="list"),
    path("~redirect/", view=ProdCategory_redirect_view, name="redirect"),
]
