from django import forms

from .models import Organisation


class OrganisationModelForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = [
            "work_org_name",
            "work_address_line1",
            "work_address_line2",
            "work_address_line3",
            "work_address_line4",
            "work_address_postcode",
            "country",
            "language",
            "currency",
        ]
        exclude = [
            "is_verified",
            "is_access_enabled",
            "is_active",
            "dateTimeModified",
            "dateTimeCreated",
            "created_by",
            "subscriptionType",
        ]
        widgets = {
            "work_org_name": forms.CharField(
                attrs={"class": "form-control", "placeholder": "Work Organisation Name"}
            ),
            "work_address_line1": forms.CharField(
                attrs={"class": "form-control", "placeholder": "Address Line 1"}
            ),
            "work_address_line2": forms.CharField(
                attrs={"class": "form-control", "placeholder": "Address Line 2"}
            ),
            "work_address_line3": forms.CharField(
                attrs={"class": "form-control", "placeholder": "Address Line 3"}
            ),
            "work_address_line4": forms.CharField(
                attrs={"class": "form-control", "placeholder": "Address Line 4"}
            ),
            "work_address_postcode": forms.CharField(
                attrs={"class": "form-control", "placeholder": "PostCode"}
            ),
            "country": forms.Select(attrs={"class": "form-control"}),
            "language": forms.Select(attrs={"class": "form-control"}),
            "currency": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_work_org_name(self):
        # update field validations here..
        data = self.cleaned_data.get("work_org_name")
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data

    def clean_work_address_line1(self):
        # update field validations here..
        data = self.cleaned_data.get("work_address_line1")
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data

    def clean_work_address_line2(self):
        data = self.cleaned_data("work_address_line2")
        return data

    def clean_work_address_line3(self):
        data = self.cleaned_data("work_address_line3")
        return data

    def clean_work_address_line4(self):
        data = self.cleaned_data("work_address_line4")
        return data

    def clean_work_address_postcode(self):
        data = self.cleaned_data.get("work_address_postcode")
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data
