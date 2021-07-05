from logging import PlaceHolder
from django import forms
from django.forms import widgets
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory

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
            "shipping_address1",
            "shipping_address2",
            "shipping_address3",
            "shipping_address4",
            "shipping_address_city",
            "shipping_address_state_county",
            "shipping_address_postcode",
            "shipping_address_country",
            "terms_conditions",
            "notes",
            "currency",
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
            "shipping_address1": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_address2": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_address3": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_address4": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_address_city": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_address_state_county": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "shipping_address_postcode": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "shipping_address_country": forms.Select(attrs={"class": "form-control"}),
            "terms_conditions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "4",
                    "placeholder": "Enter the terms and conditions of your business to be displayed in your transaction",
                },
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
            "currency": forms.Select(attrs={"class": "form-control"}),
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
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-control"
        self.helper = FormHelper()
        # self.helper.label_class = "col-md-3 create-label"
        # self.helper.field_class = "col-md-9"
        self.helper.layout = Layout(
            Div(
                HTML(
                    """
                    <div class="col-sm-12">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Create Quotes/Estimates</h5>
                                <small class="form-text text-muted">Your References</small>
                                <div class="form-row">
                                    <div class="form-group col-md-3">
                                        <label for="inputorg">Quote #</label>
                                        {{form.quote_id}}
                                    </div>
									<div class="form-group col-md-3">
                                        <label for="inputorg">Contact Type</label>
                                        {{form.contactType}}
                                    </div>
									<div class="form-group col-md-3">
                                        <label for="inputorg">Contact ID</label>
                                        {{form.leadId}}
                                    </div>
									<div class="form-group col-md-3">
                                        <label for="inputorg">Reference</label>
                                        {{form.reference}}
                                    </div>
                                </div>
								<hr>
                                <small class="form-text text-muted">Estimate details</small>
								<div class="form-row">
								    <div class="form-group col-md-6">
                                        <label for="inputorg">Deal Name</label>
                                        {{form.deal_name}}
                                    </div>
                                    <div class="form-group col-md-6">
                                        <label for="inputorg">Subject</label>
                                        {{form.subject}}
                                    </div>
								</div>
								<div class="form-row">
                                    <div class="form-group col-md-3">
                                        <label for="inputorg">Owner</label>
                                        {{form.owner}}
                                    </div>
									<div class="form-group col-md-3">
                                        <label for="inputorg">Valif From</label>
                                        {{form.start_date}}
                                    </div>
									<div class="form-group col-md-3">
                                        <label for="inputorg">Valid Until</label>
                                        {{form.end_date}}
                                    </div>
									<div class="form-group col-md-3">
                                        <label for="inputorg">Stage</label>
                                        {{form.stage}}
                                    </div>
                                </div>
								<hr>
                                <small class="form-text text-muted">Customer Details</small>
								<div class="form-row">
                                    <div class="form-group col-md-4">
                                        <label for="inputorg">Title</label>
                                        {{form.title}}
                                    </div>
									<div class="form-group col-md-4">
                                        <label for="inputorg">First Name</label>
                                        {{form.first_name}}
                                    </div>
									<div class="form-group col-md-4">
                                        <label for="inputorg">Last Name</label>
                                        {{form.last_name}}
                                    </div>
                                </div>
								<div class="form-row">
									<div class="form-group col-md-6">
                                        <label for="inputorg">Organisation Name</label>
                                        {{form.work_org_name}}
                                    </div>
                                    <div class="form-group col-md-6">
                                        <label for="inputorg">Email</label>
                                        {{form.email}}
                                    </div>
								</div>
                                <p> Billing Address </p>
                                <div class="form-row">
                                    <div class="form-group col-md-3">
                                        <label for="inputwaddress1">Address Line 1</label>
                                        {{form.billing_address1}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwaddress2">Address Line 2</label>
                                        {{form.billing_address2}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwaddress3">Address Line 3</label>
                                        {{form.billing_address3}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwaddress4">Address Line 4</label>
                                        {{form.billing_address4}}
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="form-group col-md-3">
                                        <label for="inputwaddress4">City</label>
                                        {{form.billing_address_city}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwaddress4">State/County</label>
                                        {{form.billing_address_state_county}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwaddress4">Post Code</label>
                                        {{form.billing_address_postcode}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwaddress4">Country</label>
                                        {{form.billing_address_country}}
                                    </div>
                                </div>
								<hr>
                     """,
                ),
                Fieldset("", Formset("quoteItems"), css_class="form-group"),
                HTML(
                    """
                        <hr>
                        <div class="form-row">
                            <div class="form-group col-md-6">
                                <label for="inputorg">Notes</label>
                                {{form.notes}}
                            </div>
                            <div class="form-group col-md-6">
                                <div class="form-group row">
                                    <label for="inputorg"  class="col-md-4 col-form-label text-md-right">Sub Total</label>
                                    <div class="col-md-4">
                                        {{form.sub_total_amount}}
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label for="inputorg"  class="col-md-4 col-form-label text-md-right">Discount</label>
                                    <div class="col-md-4">
                                        {{form.discount}}
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label for="inputorg"  class="col-md-4 col-form-label text-md-right" >Shipping Charges</label>
                                    <div class="col-md-4">
                                        {{form.shipping_charges}}
                                    </div>
                                </div>
                                <div class="form-group row ">
                                    <label for="inputorg"  class="col-md-4 col-form-label text-md-right">VAT on shipping charges</label>
                                    <div class="col-md-4">
                                        {{form.shipping_vat}}
                                    </div>
                                </div>
                                <hr>
                                <div class="form-group  row  pt-1 font-weight-bold" >
                                    <label for="inputorg"  class="col-md-4 col-form-label text-md-right">Total Amount</label>
                                    <div class="col-md-4 ">
                                        {{form.total_amount}}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                        <div class="form-row">
                            <div class="form-group col-md-6 ml-4">
                                <label for="inputorg">Terms and Conditions</label>
                                {{form.terms_conditions}}
                            </div>
                            <div class="form-group col-md-4 ml-4">
                                <label for="inputorg">Attachments</label>
                                {{form.file}}
                            </div>
                        </div>
                        <br>
                        <div class="buttonHolder">
                            <input type="submit" name="submit" value="Create Quote" class="btn btn-primary ml-4"  style="width: 200px;" id="submit-id-submit">
                        </div>
                """,
                ),
                HTML(
                    """

                        </div>
                    </div>
                """
                ),
            )
        )


class QuotedItemModelForm(forms.ModelForm):
    class Meta:
        model = QuotedItem
        fields = [
            "item",
            "quantity",
            "amount",
            "currency",
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
            "currency": forms.Select(attrs={"class": "form-control"}),
            "discount": forms.NumberInput(
                attrs={"class": "form-control lineItemCal discount"}
            ),
            "vat_rate": forms.Select(
                attrs={"class": "form-control lineItemCal vatrate"}
            ),
            "line_total": forms.NumberInput(
                attrs={"class": "form-control lineItemCal linetotal ", "disabled": True}
            ),
        }


# QuotedItemFormSet = modelformset_factory(
#     QuotedItem,
#     QuotedItemModelForm,
#     extra=2,
#     can_delete=True,
#     min_num=1,
# )

QuoteItemsInlineFormset = inlineformset_factory(
    Quote,
    QuotedItem,
    form=QuotedItemModelForm,
    fields=[
        "item",
        "quantity",
        "amount",
        "currency",
        "discount",
        "vat_rate",
        "line_total",
    ],
    extra=1,
    can_delete=True,
)
