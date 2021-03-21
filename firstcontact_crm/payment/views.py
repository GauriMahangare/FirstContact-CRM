from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from payment.models import Pricing

# from .models import Pricing

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY



class EnrollView(generic.TemplateView):
    template_name = "payment/enroll.html"


class CheckoutView(generic.TemplateView):
    template_name = "payment/checkout.html"

### Stripe Webhook processing 
#@app.route('/stripe-webhook', methods=['POST'])
@csrf_exempt
def webhook_received(request):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']

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