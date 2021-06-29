from django.urls import path

from product.views import (
    ####### Product view ##########
    Product_create_view,
    Product_update_view,
    Product_delete_view,
    Product_list_view,
    Product_redirect_view,
)

app_name = "product"
urlpatterns = [
    ################# Categories URLS #################
    path(
        "~create/>",
        view=Product_create_view,
        name="create",
    ),
    path(
        "~update/<int:pk>",
        view=Product_update_view,
        name="update",
    ),
    path(
        "~delete/<int:pk>",
        view=Product_delete_view,
        name="delete",
    ),
    path("~list/", view=Product_list_view, name="list"),
    path("~redirect/", view=Product_redirect_view, name="redirect"),
]
