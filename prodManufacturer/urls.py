from django.urls import path

from prodManufacturer.views import (
    ####### Manufacturer view ##########
    Manufacturer_create_view,
    Manufacturer_update_view,
    Manufacturer_delete_view,
    Manufacturer_list_view,
    Manufacturer_redirect_view,
)

app_name = "manufacturer"
urlpatterns = [
    ################# Categories URLS #################
    path(
        "~create/>",
        view=Manufacturer_create_view,
        name="create",
    ),
    path(
        "~update/<int:pk>",
        view=Manufacturer_update_view,
        name="update",
    ),
    path(
        "~delete/<int:pk>",
        view=Manufacturer_delete_view,
        name="delete",
    ),
    path("~list/", view=Manufacturer_list_view, name="list"),
    path("~redirect/", view=Manufacturer_redirect_view, name="redirect"),
]
