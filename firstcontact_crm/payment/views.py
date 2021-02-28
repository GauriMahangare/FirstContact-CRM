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

# from .models import Pricing

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY



class EnrollView(generic.TemplateView):
    template_name = "payment/enroll.html"


class CheckoutView(generic.TemplateView):
    template_name = "payment/checkout.html"