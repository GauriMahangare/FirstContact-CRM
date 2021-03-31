from datetime import datetime
from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from pytz import utc
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from stripe.api_resources.subscription import Subscription
from waffle.decorators import waffle_flag,flag_is_active
from waffle.mixins import WaffleFlagMixin

import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from payment.models import Pricing

# from .models import Pricing

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


class EnrollView(generic.TemplateView):
    template_name = "payment/enroll.html"


# class CheckoutView(generic.TemplateView):
#     template_name = "payment/checkout.html"


def CheckoutView(request, slug):
    current_pricing = request.user.subscription.pricing.name
    pricing = get_object_or_404(Pricing, slug=slug)
    context = {
                "pricing_tier": pricing,
                "current_subscription": current_pricing,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    } 
    return render(request, "payment/checkout.html", context)  
        

### Stripe Webhook processing 
#@app.route('/stripe-webhook', methods=['POST'])

@csrf_exempt
def webhook_received(request):
    print("webhook received")
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    # webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    # print("webhook received")
    # payload = request.body
    #  # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
    # signature = request.META["HTTP_STRIPE_SIGNATURE"]

    # if webhook_secret:   
    #     #signature = request.headers.get('stripe-signature')
    #     try:
    #         event = stripe.Webhook.construct_event(
    #             ayload=payload, sig_header=signature, secret=webhook_secret)
    #         data = event['data']
    #     except Exception as e:
    #         return e
    #     # Get the type of webhook event sent - used to check the status of PaymentIntents.
    #     event_type = event['type']
    # else:
    #     data = payload['data']
    #     event_type = payload['type']

    # data_object = data['object']

    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
    signature = request.META["HTTP_STRIPE_SIGNATURE"]
    
    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=webhook_secret)
        data = event['data']
        print("signature verified")
    except Exception as e:
        print(str(e))
        return e
        
    # Get the type of webhook event sent - used to check the status of PaymentIntents.
    event_type = event['type']
    data_object = data['object']

    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        # TODO: change the users subscription and pricing
        print(data)

        webhook_object = data["object"]
        stripe_customer_id = webhook_object["customer"]

        stripe_sub = stripe.Subscription.retrieve(webhook_object["subscription"])
        stripe_price_id = stripe_sub["plan"]["id"]

        pricing = Pricing.objects.get(stripe_price_id=stripe_price_id)

        user = User.objects.get(stripe_customer_id=stripe_customer_id)
        user.subscription.status = stripe_sub["status"]
        user.subscription.stripe_subscription_id = webhook_object["subscription"]
        user.subscription.pricing = pricing
        user.subscription.slug = user.username +"-"+ pricing.name
        now = datetime.now()
        nowDate = now.replace(tzinfo=utc)
        user.subscription.freeTrialEndDate = nowDate
        user.subscription.save()

    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        print(data)

    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print(data)
        webhook_object = data["object"]
        stripe_customer_id = webhook_object["customer"]
        stripe_sub = stripe.Subscription.retrieve(webhook_object["id"])
        user = User.objects.get(stripe_customer_id=stripe_customer_id)
        user.subscription.status = stripe_sub["status"]
        user.subscription.save()

    if event_type == 'invoice.finalized':
        # If you want to manually send out invoices to your customers
        # or store them locally to reference to avoid hitting Stripe rate limits.
        print(data)

    if event_type == 'customer.subscription.trial_will_end':
        # Send notification to your user that the trial will end
        print(data)

    if event_type == 'customer.subscription.updated':
        print(data)
        
    #return jsonify({'status': 'success'})
    return HttpResponse()

class CreateSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = request.user.stripe_customer_id
        try:
            # Attach the payment method to the customer
            stripe.PaymentMethod.attach(
                data['paymentMethodId'],
                customer=customer_id,
            )
            # Set the default payment method on the customer
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': data['paymentMethodId'],
                },
            )

            # Create the subscription
            subscription = stripe.Subscription.create(
                default_payment_method=data['paymentMethodId'],
                customer=customer_id,
                items=[{'price': data["priceId"]}],
                expand=['latest_invoice.payment_intent'],
            )

            # new_subscription = Subscription.objects.get_or_create(user=request.user)
            # print(new_subscription.user)
            data = {}
            data.update(subscription)
            return Response(data)

        except Exception as e:
            return Response({
                "error": {'message': str(e)}
            })

class ChangeSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        subscription_id = request.user.subscription.stripe_subscription_id
        subscription = stripe.Subscription.retrieve(subscription_id)
        try:
            updatedSubscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': request.data["priceId"],
                }],
                proration_behavior="always_invoice"
            )

            data = {}
            data.update(updatedSubscription)
            return Response(data)
        except Exception as e:
            return Response({
                "error": {'message': str(e)}
            })

class RetryInvoiceView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = request.user.stripe_customer_id
        try:

            stripe.PaymentMethod.attach(
                data['paymentMethodId'],
                customer=customer_id,
            )
            # Set the default payment method on the customer
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': data['paymentMethodId'],
                },
            )

            invoice = stripe.Invoice.retrieve(
                data['invoiceId'],
                expand=['payment_intent'],
            )
            data = {}
            data.update(invoice)

            return Response(data)
        except Exception as e:

            return Response({
                "error": {'message': str(e)}
            })

class CancelSubscription(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.data)
        customer_id = request.user.stripe_customer_id
        try:
            # Cancel the subscription by deleting it
            deletedSubscription = stripe.Subscription.delete(data['subscriptionId'])
            data = {}
            data.update(deletedSubscription)
            return Response(data)
        except Exception as e:
              return Response({
                "error": {'message': str(e)}
            })

class ReceiveUpcomingInvoice(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.data)
        customer_id = request.user.stripe_customer_id
        try:    
            # Retrieve the subscription
            subscription = stripe.Subscription.retrieve(data['subscriptionId'])

            # Retrieve the invoice
            invoice = stripe.Invoice.upcoming(
                customer=data['customerId'],
                subscription=data['subscriptionId'],
                subscription_items=[
                    {
                        'id': subscription['items']['data'][0].id,
                        'deleted': True,
                    },
                    {
                        'price': 'price_H1NlVtpo6ubk0m',
                        'deleted': False,
                    }
                ],
            )  
            data = {}
            data.update(invoice)

            return Response(data)
        except Exception as e:

            return Response({
                "error": {'message': str(e)}
            })
class RetrieveCustomerPaymentMethod(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.data)
        customer_id = request.user.stripe_customer_id
        try:
            paymentMethod = stripe.PaymentMethod.retrieve(
                data['paymentMethodId'],
            )
            data = {}
            data.update(paymentMethod)

            return Response(data)
        except Exception as e:

            return Response({
                "error": {'message': str(e)}
            })