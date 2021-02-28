from django.urls import path
from .views import (
    EnrollView, 
    CheckoutView,
)

app_name = "payment"

urlpatterns = [
    path('enroll/', EnrollView.as_view(), name='enroll'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]