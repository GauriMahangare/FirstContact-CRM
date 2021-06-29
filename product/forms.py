from prodCategory.models import ProdCategory
from prodManufacturer.models import Manufacturer
from category.models import Category
from django import forms
from django.contrib.auth import get_user_model
from .models import Product
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "image",
            "owner",
            "handler",
            "code",
            "name",
            "category",
            "isActive",
            "manufacturer",
            "sale_start_date",
            "sale_end_date",
            "support_start_date",
            "support_end_date",
            "unit_price",
            "currency",
            "comission_rate",
            "tax",
            "isTaxable",
            "usage_unit",
            "quantity_in_stock",
            "quantity_ordered",
            "reorder_level",
            "quantity_in_demand",
            "description",
        ]
        exclude = [
            "dateTimeModified",
            "dateTimeCreated",
            "created_by",
            "organisation",
        ]
        widgets = {
            "image": forms.widgets.ClearableFileInput(
                attrs={"class": "form-control-file"}
            ),
            "owner": forms.Select(attrs={"class": "form-control"}),
            "handler": forms.Select(attrs={"class": "form-control"}),
            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "isActive": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "manufacturer": forms.Select(attrs={"class": "form-control"}),
            "sale_start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "sale_end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "support_start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "support_end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "currency": forms.Select(attrs={"class": "form-control"}),
            "comission_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "tax": forms.NumberInput(attrs={"class": "form-control"}),
            "isTaxable": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "usage_unit": forms.Select(attrs={"class": "form-control"}),
            "quantity_in_stock": forms.NumberInput(attrs={"class": "form-control"}),
            "quantity_ordered": forms.NumberInput(attrs={"class": "form-control"}),
            "reorder_level": forms.TextInput(attrs={"class": "form-control"}),
            "quantity_in_demand": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        user_org = kwargs.pop("user_org", None)
        super(ProductModelForm, self).__init__(*args, **kwargs)
        users_in_org = User.objects.none()

        users_in_org = User.objects.filter(userorganization=user_org)
        category_in_org = ProdCategory.objects.none()
        category_in_org = ProdCategory.objects.filter(organisation=user_org)
        manufacturer_in_org = Manufacturer.objects.none()
        manufacturer_in_org = Manufacturer.objects.filter(organisation=user_org)

        self.fields["owner"].queryset = users_in_org
        self.fields["handler"].queryset = users_in_org
        self.fields["category"].queryset = category_in_org
        self.fields["manufacturer"].queryset = manufacturer_in_org

    def clean(self):
        cleaned_data = super().clean()
        sale_end_date = self.cleaned_data.get("sale_end_date")
        sale_start_date = self.cleaned_data.get("sale_start_date")
        support_end_date = self.cleaned_data.get("support_end_date")
        support_start_date = self.cleaned_data.get("support_start_date")
        msg = "End date cannot be less than start date."
        if sale_end_date and sale_start_date and sale_end_date < sale_start_date:
            self.add_error("sale_end_date", msg)

        if (
            support_end_date
            and support_start_date
            and support_end_date < support_start_date
        ):
            self.add_error("support_end_date", msg)
