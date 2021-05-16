from datetime import datetime
import logging
import json
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from rest_framework.views import APIView
from rest_framework.response import Response

from waffle.decorators import waffle_flag,flag_is_active
from waffle.mixins import WaffleFlagMixin

import stripe

from payment.models import Subscription,Pricing,PaymentMethod
from payment.forms import PaymentMethodModelForm


User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


class EnrollView(LoginRequiredMixin,SuccessMessageMixin,generic.TemplateView):
    template_name = "payment/enroll.html"


# class CheckoutView(generic.TemplateView):
#     template_name = "payment/checkout.html"

@login_required()
def CheckoutView(request, slug):
    current_pricing = request.user.subscription.pricing.name
    subscription = request.user.subscription
    pricing = get_object_or_404(Pricing, slug=slug)
    context = {
                "pricing_tier": pricing,
                "current_subscription": current_pricing,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }

    if subscription.is_active:
        return render(request, "payment/change.html", context)
    return render(request, "payment/checkout.html", context)

@login_required()
def PaymentMethodAddCheckoutView(request, slug):
    current_pricing = request.user.subscription.pricing.name
    subscription = request.user.subscription
    pricing = get_object_or_404(Pricing, slug=slug)
    context = {
                "pricing_tier": pricing,
                "current_subscription": current_pricing,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, "payment/addPaymentMethod.html", context)

@login_required()
def PaymentMethodUpdateView(request,pk):
    context = {}
    try:
        pmt_mthd_obj = PaymentMethod.objects.get(pk=pk)
    except PaymentMethod.DoesNotExist:
        logger.critical("Payment Method does not exists")
        raise Http404
    else:
        form = PaymentMethodModelForm(request.POST or None , instance = pmt_mthd_obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            form.save()
            pmt_mthd_obj = PaymentMethod.objects.get(pk=pk)
            exp_mth_int = int(obj.expiry_month)
            exp_year_int = int(obj.expiry_year)
            try:
                stripe.PaymentMethod.modify(
                    pmt_mthd_obj.stripe_payment_method_id,
                    card={"exp_month": exp_mth_int,
                          "exp_year" : exp_year_int
                    }
                )
            except:
                logger.critical("Stripe payment method update error for card")
            else:
                logger.info("Stripe payment method update successful for card")
            # messages.success(self.request, "Payment method has been updated")
            # return reverse("users:subscription", kwargs={"username": self.request.user.username})
                return HttpResponseRedirect('/users/~subscription/redirect/')
        context={
            "form":form,
            "obj":pmt_mthd_obj
            }
        return render(request, "payment/updatePaymentMethod.html", context)

### Stripe Webhook processing
#@app.route('/stripe-webhook', methods=['POST'])

@csrf_exempt
def webhook_received(request):
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
        logger.info('Webhook Signature verified')
    except Exception as e:
        print(str(e))
        logger.critical('Webhook signture could not be verified',exc_info=1)
        return e

    # Get the type of webhook event sent - used to check the status of PaymentIntents.
    event_type = event['type']
    event_id = event['id']
    data_object = data['object']
    logger.info('Webhook Received - %s - %s',event_id,event_type)


    if event_type == 'customer.updated':
        logger.info('Customer Updated')

    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        # TODO: change the users subscription and pricing

        logger.info('Invoice Paid')
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
        #nowDate = now.replace(tzinfo=utc)
        user.subscription.freeTrialEndDate = now
        user.subscription.period_start = datetime.utcfromtimestamp(stripe_sub.current_period_start)
        user.subscription.period_end = datetime.utcfromtimestamp(stripe_sub.current_period_end)
        user.payment_status = webhook_object["status"]
        user.subscription.save()

        try:
            pmt_methods=stripe.PaymentMethod.list(
                        customer=user.stripe_customer_id,
                        type="card",
            )
        except:
            logger.critical('Payment methods not found for %s' , user.pk )
        else:
            logger.info('Successfully retrieved payment methods for %s' , user.pk)
            pmt_method_data =  pmt_methods["data"]

            for method in pmt_method_data:
                obj, created = PaymentMethod.objects.update_or_create(
                        user = user,
                        stripe_payment_method_id = method.id,
                        defaults={
                            'user' : user,
                            'subscription' : user.subscription,
                            'stripe_payment_method_id' : method.id,
                            'type' : method.type,
                            'brand' : method.card.brand,
                            'country' : method.card.country,
                            'expiry_month' : method.card.exp_month,
                            'expiry_year' : method.card.exp_year,
                            'last4': method.card.last4,
                            'is_default' : False,
                            'fingerprint' : method.card.fingerprint
                        }
                    )
                print(obj)
                print(created)
                if created:
                    try:
                        pmt_mthd = PaymentMethod.objects.get(stripe_payment_method_id = method.id)
                    except:
                        logger.critical('Payment method not found for %s' , user.pk )
                    else:
                        logger.info('Payment method found for %s' , user.pk )
                        pmt_mthd.is_default = True
                        pmt_mthd.save()

    if event_type == 'payment_method.updated':
        # Payment Methods table also updated to reflect the same.
        logger.info('Payment method updated')
        webhook_object = data["object"]
        stripe_customer_id = webhook_object["customer"]
        user = User.objects.get(stripe_customer_id=stripe_customer_id)
        try:
            pmt_methods=stripe.PaymentMethod.list(
                        customer=user.stripe_customer_id,
                        type="card",
            )
        except:
            logger.critical('Payment methods not found for %s' , user.pk )
        else:
            logger.info('Successfully retrieved payment methods for %s' , user.pk)
            pmt_method_data =  pmt_methods["data"]

            for method in pmt_method_data:
                obj, created = PaymentMethod.objects.update_or_create(
                        user = user,
                        stripe_payment_method_id = method.id,
                        defaults={
                            'user' : user,
                            'subscription' : user.subscription,
                            'stripe_payment_method_id' : method.id,
                            'type' : method.type,
                            'brand' : method.card.brand,
                            'country' : method.card.country,
                            'expiry_month' : method.card.exp_month,
                            'expiry_year' : method.card.exp_year,
                            'last4': method.card.last4,
                            'is_default' : False,
                            'fingerprint' : method.card.fingerprint
                        }
                    )
                if created:
                    try:
                        pmt_mthd = PaymentMethod.objects.get(stripe_payment_method_id = method.id)
                    except:
                        logger.critical('Payment method not found for %s' , user.pk )
                    else:
                        logger.info('Payment method found for %s' , user.pk )
                        pmt_mthd.is_default = True
                        pmt_mthd.save()


    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        # Do we revert back to free for life subscription here?
        logger.info('Payment failed')

    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        # Do we revert back to free for life subscription here?
        logger.info('Subscription cancelled')
        webhook_object = data["object"]
        stripe_customer_id = webhook_object["customer"]
        stripe_sub = stripe.Subscription.retrieve(webhook_object["id"])
        user = User.objects.get(stripe_customer_id=stripe_customer_id)
        pricing = get_object_or_404(Pricing,name="FreeForLife")
        user.subscription.pricing = pricing
        user.subscription.status = ""
        user.subscription.nextPaymentDueDate = ""
        user.subscription.save()

    if event_type == 'invoice.finalized':
        # If you want to manually send out invoices to your customers
        # or store them locally to reference to avoid hitting Stripe rate limits.
        # Do we store invoices locallY?
        logger.info('Invoice finalised')

    if event_type == 'customer.subscription.trial_will_end':
        # Send notification to your user that the trial will end
        logger.info('Subscription Trial ended')

    if event_type == 'customer.subscription.updated':
        logger.info('Subscription Updated')
        webhook_object = data["object"]
        print(webhook_object["status"])
        stripe_customer_id = webhook_object["customer"]
        stripe_sub = stripe.Subscription.retrieve(webhook_object["id"])
        stripe_price_id = stripe_sub["plan"]["id"]
        user = User.objects.get(stripe_customer_id=stripe_customer_id)
        try:
            pricing = Pricing.objects.get(stripe_price_id=stripe_price_id)
        except Exception as e:
            print(str(e))
            logger.critical('Pricing Id {stripe_price_id} not found',exc_info=1)
        else:
            user.subscription.pricing = pricing
            user.subscription.slug = user.username +"-"+ pricing.name
            user.subscription.status = stripe_sub["status"]
            user.subscription.period_start = datetime.utcfromtimestamp(stripe_sub.current_period_start)
            user.subscription.period_end = datetime.utcfromtimestamp(stripe_sub.current_period_end)
            user.payment_status = webhook_object["status"]
            user.subscription.save()


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

            data = {}
            data.update(subscription)

            return Response(data)

        except Exception as e:
            return Response({
                "error": {'message': str(e)}
            })

class ChangeSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        customer_id = request.user.stripe_customer_id
        subscription_id = request.user.subscription.stripe_subscription_id
        subscription = stripe.Subscription.retrieve(subscription_id)
        try:
            updatedSubscription = stripe.Subscription.modify(
                subscription.id,
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
        data = request.data
        #customer_id = request.user.stripe_customer_id
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
        data = request.data
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