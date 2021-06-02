
from django.urls import path
from django.conf.urls import url

from leads.views import (
    Lead_redirect_view,
    Lead_update_view,
    Lead_create_view,
    Lead_list_view,
    Lead_detail_view,
    multi_lead_delete_view,
)

app_name = "leads"
urlpatterns = [
    path("~update/<uuid:pk>", view=Lead_update_view, name="update"),
    path("~create/", view=Lead_create_view, name="create"),
    #path("~delete/<uuid:pk>", view=Lead_delete_view, name="delete"),
    path("confirm-delete", view=multi_lead_delete_view, name="deleteconfirm"),
    # url(r'^confirm-delete$', multi_lead_delete_view, name='deleteconfirm', kwargs={"leads_tobe_deleted": None}),
    path("~list/", view=Lead_list_view, name="list"),
    path("~detail/<uuid:pk>", view=Lead_detail_view, name="detail"),
    path("~redirect/", view=Lead_redirect_view, name="redirect"),
]
