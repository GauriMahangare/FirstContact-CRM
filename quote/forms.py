from typing import Sequence
from django import forms
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory

from .models import QuotedItem, Quote
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Field,
    Fieldset,
    Div,
    HTML,
    ButtonHolder,
    Row,
    Submit,
)
from crispy_forms.bootstrap import Tab, TabHolder
from .custom_layout_object import *


class QuoteModelForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = [
            "quote_id",
            "contactType",
            "leadId",
            "reference",
            "owner",
            "deal_name",
            "subject",
            "start_date",
            "end_date",
            "stage",
            "title",
            "first_name",
            "last_name",
            "work_org_name",
            "billing_address1",
            "billing_address2",
            "billing_address3",
            "billing_address4",
            "billing_address_city",
            "billing_address_state_county",
            "billing_address_postcode",
            "billing_address_country",
            "terms_conditions",
            "notes",
            "sub_total_amount",
            "discount",
            "shipping_charges",
            "shipping_vat",
            "adjustment",
            "total_amount",
            "file",
            "email",
        ]
        exclude = [
            "organisation",
            "created_by",
            "modified_by",
            "dateTimeModified",
            "dateTimeCreated",
        ]
        widgets = {
            "quote_id": forms.TextInput(attrs={"class": "form-control"}),
            "contactType": forms.Select(attrs={"class": "form-control"}),
            "leadId": forms.Select(attrs={"class": "form-control"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
            "owner": forms.Select(attrs={"class": "form-control"}),
            "deal_name": forms.TextInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "stage": forms.Select(attrs={"class": "form-control"}),
            "title": forms.Select(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "work_org_name": forms.TextInput(attrs={"class": "form-control"}),
            "billing_address1": forms.TextInput(attrs={"class": "form-control"}),
            "billing_address2": forms.TextInput(attrs={"class": "form-control"}),
            "billing_address3": forms.TextInput(attrs={"class": "form-control"}),
            "billing_address4": forms.TextInput(attrs={"class": "form-control"}),
            "billing_address_city": forms.TextInput(attrs={"class": "form-control"}),
            "billing_address_state_county": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "billing_address_postcode": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "billing_address_country": forms.Select(attrs={"class": "form-control"}),
            "terms_conditions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "4",
                    "placeholder": "Enter the terms and conditions of your business to be displayed in your transaction",
                },
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "4",
                    "placeholder": "Thank you for your business.",
                }
            ),
            "sub_total_amount": forms.NumberInput(
                attrs={"class": "form-control", "disabled": True}
            ),
            "discount": forms.NumberInput(attrs={"class": "form-control"}),
            "shipping_charges": forms.NumberInput(attrs={"class": "form-control"}),
            "shipping_vat": forms.Select(attrs={"class": "form-control"}),
            "adjustment": forms.NumberInput(attrs={"class": "form-control"}),
            "total_amount": forms.NumberInput(
                attrs={"class": "form-control", "disabled": True}
            ),
            "file": forms.widgets.ClearableFileInput(
                attrs={
                    "class": "form-control-file btn-primary",
                }
            ),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(QuoteModelForm, self).__init__(*args, **kwargs)


class QuotedItemModelForm(forms.ModelForm):
    class Meta:
        model = QuotedItem
        fields = [
            "item",
            "quantity",
            "amount",
            # "currency",
            "discount",
            "vat_rate",
            "line_total",
        ]
        exclude = [
            "quote",
            "created_by",
            "modified_by",
            "dateTimeModified",
            "dateTimeCreated",
        ]
        widgets = {
            "item": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control lineItemCal quantity"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control lineItemCal amount"}
            ),
            "discount": forms.NumberInput(
                attrs={"class": "form-control lineItemCal discount"}
            ),
            "vat_rate": forms.Select(
                attrs={"class": "form-control lineItemCal vatrate"}
            ),
            "line_total": forms.NumberInput(
                attrs={
                    "class": "form-control lineItemCal linetotal ",
                    "disabled": True,
                    "value": 0,
                }
            ),
        }


QuotedItemFormSet = modelformset_factory(
    QuotedItem,
    QuotedItemModelForm,
    extra=1,
    can_delete=True,
    min_num=1,
)
QuoteFormSet = inlineformset_factory(
    Quote, QuotedItem, form=QuotedItemModelForm, extra=1, can_delete=True
)
