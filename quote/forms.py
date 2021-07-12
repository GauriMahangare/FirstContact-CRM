from vatRate.models import VatRate
from product.models import Product
from typing import Sequence
from django import forms
from django.forms import modelformset_factory
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory

from .models import QuotedItem, Quote, Stage
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

User = get_user_model()


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
        user = kwargs.pop("user", None)
        user_org = kwargs.pop("user_org", None)
        super(QuoteModelForm, self).__init__(*args, **kwargs)

        users_in_org = User.objects.none()
        users_in_org = User.objects.exclude(userorganization=None).filter(
            userorganization=user_org
        )
        self.fields["owner"].queryset = users_in_org

        vatrate_in_org = VatRate.objects.none()
        vatrate_in_org = VatRate.objects.filter(organisation=user_org)
        self.fields["shipping_vat"].queryset = vatrate_in_org
        stage_in_org = Stage.objects.none()
        stage_in_org = Stage.objects.filter(organisation=user_org)
        self.fields["stage"].queryset = stage_in_org

    def clean_discount(self):
        # update field validations here..
        data = self.cleaned_data.get("discount")
        if data < 0:
            raise forms.ValidationError("This field needs to be a +ve number")
        return data

    def clean_shipping_charges(self):
        # update field validations here..
        data = self.cleaned_data.get("shipping_charges")
        if data < 0:
            raise forms.ValidationError("This field needs to be a +ve number")
        return data

    def clean_adjustment(self):
        # update field validations here..
        data = self.cleaned_data.get("adjustment")
        if data < 0:
            raise forms.ValidationError("This field needs to be a +ve number")
        return data


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

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop("user", None)
        self.user_org = kwargs.pop("user_org", None)
        super(QuotedItemModelForm, self).__init__(*args, **kwargs)
        products_in_org = Product.objects.none()
        products_in_org = Product.objects.filter(organisation=self.user_org)
        self.fields["item"].queryset = products_in_org
        vatrate_in_org = VatRate.objects.none()
        vatrate_in_org = VatRate.objects.filter(organisation=self.user_org)
        self.fields["vat_rate"].queryset = vatrate_in_org

    def clean_item(self):
        # update field validations here..
        data = self.cleaned_data.get("item")
        if data is None:
            raise forms.ValidationError("This field is required")
        return data

    def clean_quantity(self):
        # update field validations here..
        data = self.cleaned_data.get("quantity")
        if data == 0:
            raise forms.ValidationError("This field is required")
        if data < 0:
            raise forms.ValidationError("This field needs to be a +ve number")
        return data

    def clean_amount(self):
        # update field validations here..
        data = self.cleaned_data.get("amount")
        if data == 0:
            raise forms.ValidationError("This field is required")
        if data < 0:
            raise forms.ValidationError("This field needs to be a +ve number")
        return data

    def clean_discount(self):
        # update field validations here..
        data = self.cleaned_data.get("discount")
        if data < 0:
            raise forms.ValidationError("This field needs to be a +ve number")
        return data


BaseQuotedItemFormSet = modelformset_factory(
    QuotedItem,
    QuotedItemModelForm,
    extra=0,
    can_delete=True,
    min_num=1,
    max_num=20,
)


class QuotedItemFormSet(BaseQuotedItemFormSet):  # sub class it
    def __init__(self, *args, **kwargs):
        #  create a user attribute and take it out from kwargs
        # so it doesn't messes up with the other formset kwargs
        self.user = kwargs.pop("user")
        self.user_org = kwargs.pop("user_org")
        super(QuotedItemFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, *args, **kwargs):
        # inject user in each form on the formset
        kwargs["user"] = self.user
        kwargs["user_org"] = self.user_org
        return super(QuotedItemFormSet, self)._construct_form(*args, **kwargs)
