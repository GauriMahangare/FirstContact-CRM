from django.urls import path
from .views import (
    EnrollView,
    CheckoutView,
    CreateSubscriptionView,
    webhook_received,
    ChangeSubscriptionView,
    RetryInvoiceView,
    ReceiveUpcomingInvoice,
    RetrieveCustomerPaymentMethod,
    CancelSubscription,
    PaymentMethodAddCheckoutView,
    PaymentMethodUpdateView,
)

app_name = "payment"

urlpatterns = [
    path('enroll/', EnrollView.as_view(), name='enroll'),
    path('enroll/<slug>/', CheckoutView, name='checkout'),
    path('paymentMethodAdd/<slug>/', PaymentMethodAddCheckoutView, name='PaymentMethodAddCheckout'),
    path('PaymentMethodUpdate/<int:pk>',PaymentMethodUpdateView,name='PaymentMethodUpdate'),
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create-subscription'),
    path('webhook/', webhook_received, name='webhook'),
    path('change-subscription/', ChangeSubscriptionView.as_view(), name='change-subscription'),
    path('retry-invoice/', RetryInvoiceView.as_view(), name='retry-invoice'),
    path('retrieve-upcoming-invoice/',ReceiveUpcomingInvoice.as_view(), name='retrieve-upcoming-invoice'),
    path('retrieve-customer-payment-method/',RetrieveCustomerPaymentMethod.as_view(), name='retrieve-customer-payment-method'),
    path('cancel-subscription/',CancelSubscription.as_view(), name='cancel-subscription'),



]
