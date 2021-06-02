from datetime import timezone
from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, HTML, Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import Tab, TabHolder, FormActions

from .models import Lead
from django.contrib.auth import get_user_model

User = get_user_model()


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "team",
            "assigned_to",
            "source",
            "title",
            "first_name",
            "last_name",
            "date_of_birth",
            "age",
            "work_org_name",
            "work_address1",
            "work_address2",
            "work_address3",
            "work_address4",
            "work_address_city",
            "work_address_state_county",
            "work_address_postcode",
            "work_address_country",
            "phone_number",
            "work_Role",
            "website",
            "mobile_number",
            "preferred_contact_preference",
            "preferred_contact_time",
            "email",
            "secondary_email",
            "social_media_1",
            "social_media_2",
            "social_media_3",
            "profile_picture",
            "status",
            "lead_Ratings",
            "description",
            "closeReason",
            "external_ref1",
            "external_ref2",
            "external_ref3",
        ]
        exclude = [
            'id',
            'created_by',
            'dateTimeModified',
            'dateTimeCreated',
        ]
        autocomplete_fields = ['status']
        widgets = {
            "team": forms.Select(attrs={'class': 'form-control'}),
            "assigned_to": forms.Select(attrs={'class': 'form-control'}),
            "source": forms.TextInput(attrs={'class': 'form-control'}),
            "title": forms.Select(attrs={'class': 'form-control'}),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "date_of_birth": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "age": forms.NumberInput(attrs={'class': 'form-control'}),
            'work_org_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Work Organisation Name'}),
            'work_address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'work_address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'work_address_line3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 3'}),
            'work_address_line4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 4'}),
            "work_address_city": forms.TextInput(attrs={'class': 'form-control'}),
            "work_address_state_county": forms.TextInput(attrs={'class': 'form-control'}),
            'work_address_postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PostCode'}),
            "work_address_country": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.NumberInput(attrs={'class': 'form-control'}),
            "work_Role": forms.TextInput(attrs={'class': 'form-control'}),
            "website": forms.URLInput(attrs={'class': 'form-control'}),
            "mobile_number": forms.NumberInput(attrs={'class': 'form-control'}),
            "preferred_contact_preference": forms.Select(attrs={'class': 'form-control'}),
            "preferred_contact_time": forms.Select(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "secondary_email": forms.EmailInput(attrs={'class': 'form-control'}),
            "social_media_1": forms.URLInput(attrs={'class': 'form-control'}),
            "social_media_2": forms.URLInput(attrs={'class': 'form-control'}),
            "social_media_3": forms.URLInput(attrs={'class': 'form-control'}),
            "profile_picture": forms.widgets.ClearableFileInput(),
            "status": forms.Select(attrs={'class': 'form-control'}),
            "lead_Ratings": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "closeReason": forms.Textarea(attrs={'class': 'form-control'}),
            "external_ref1": forms.TextInput(attrs={'class': 'form-control'}),
            "external_ref2": forms.TextInput(attrs={'class': 'form-control'}),
            "external_ref3": forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_work_org_name(self):
        # update field validations here..
        data = self.cleaned_data.get('work_org_name')
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data

    def clean_work_address_line1(self):
        # update field validations here..
        data = self.cleaned_data.get('work_address_line1')
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data

    def clean_work_address_line2(self):
        data = self.cleaned_data('work_address_line2')
        return data

    def clean_work_address_line3(self):
        data = self.cleaned_data('work_address_line3')
        return data

    def clean_work_address_line4(self):
        data = self.cleaned_data('work_address_line4')
        return data

    def clean_work_address_postcode(self):
        data = self.cleaned_data.get('work_address_postcode')
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data

    def __init__(self, *args, **kwargs):
        super(LeadModelForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        users_in_org = User.objects.none()
        if instance:
            users_in_org = User.objects.filter(userorganization_id=instance.organisation_id)

        self.fields['assigned_to'].queryset = users_in_org
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('Personal Information',
                    HTML("""
                        {% if form.profile_picture.value %}
                            <img class="center img-thumbnail" width="100" height="100" crop="center" src="{{ MEDIA_URL }}{{ form.profile_picture.value }}" >
                        {% endif %}
                    """, ),
                    'profile_picture',
                    'title',
                    'first_name',
                    'last_name',
                    'date_of_birth',
                    'age'
                    ),
                Tab('Company Data',
                    'work_org_name',
                    'work_address1',
                    'work_address2',
                    'work_address3',
                    'work_address4',
                    'work_address_city',
                    'work_address_state_county',
                    'work_address_postcode',
                    'work_address_country',
                    'work_Role',
                    'website'
                    ),
                Tab('Contact Information',
                    'phone_number',
                    'mobile_number',
                    'preferred_contact_preference',
                    'preferred_contact_time',
                    'email',
                    'secondary_email',
                    'social_media_1',
                    'social_media_2',
                    'social_media_3',
                    ),
                Tab(
                    'Manage Lead',
                    'status',
                    'team',
                    'assigned_to',
                    'source',
                    'lead_Ratings',
                    'description',
                    'closeReason',
                ),
                Tab(
                    'Additional Information',
                    'external_ref1',
                    'external_ref2',
                    'external_ref3',
                )
            )
        )
        self.helper.layout.append(Submit('submit', 'Update Lead')

                                  )
