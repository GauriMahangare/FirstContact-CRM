from django import forms
from .models import Lead, Note
from category.models import Category
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    Layout,
    Submit,
)
from crispy_forms.bootstrap import Tab, TabHolder

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
            "emailOptIn",
            "nbr_of_employees",
            "industry",
            "annual_revenue",
            "currency",
            "preferred_communication_language",
        ]
        exclude = [
            "id",
            "created_by",
            "dateTimeModified",
            "dateTimeCreated",
            "emailOptInStatusChangeDate",
        ]
        autocomplete_fields = ["status", "industry", "assigned_to"]
        widgets = {
            "team": forms.Select(attrs={"class": "form-control"}),
            "assigned_to": forms.Select(attrs={"class": "form-control"}),
            "source": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.Select(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "work_org_name": forms.TextInput(attrs={"class": "form-control"}),
            "work_address1": forms.TextInput(attrs={"class": "form-control"}),
            "work_address2": forms.TextInput(attrs={"class": "form-control"}),
            "work_address3": forms.TextInput(attrs={"class": "form-control"}),
            "work_address4": forms.TextInput(attrs={"class": "form-control"}),
            "work_address_city": forms.TextInput(attrs={"class": "form-control"}),
            "work_address_state_county": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "work_address_postcode": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "PostCode"}
            ),
            "work_address_country": forms.Select(attrs={"class": "form-control"}),
            "phone_number": forms.NumberInput(attrs={"class": "form-control"}),
            "work_Role": forms.TextInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "mobile_number": forms.NumberInput(attrs={"class": "form-control"}),
            "preferred_contact_preference": forms.Select(
                attrs={"class": "form-control"}
            ),
            "preferred_contact_time": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "secondary_email": forms.EmailInput(attrs={"class": "form-control"}),
            "social_media_1": forms.URLInput(attrs={"class": "form-control"}),
            "social_media_2": forms.URLInput(attrs={"class": "form-control"}),
            "social_media_3": forms.URLInput(attrs={"class": "form-control"}),
            "profile_picture": forms.widgets.ClearableFileInput(
                attrs={"class": "form-control-file"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "lead_Ratings": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "closeReason": forms.Textarea(attrs={"class": "form-control"}),
            "external_ref1": forms.TextInput(attrs={"class": "form-control"}),
            "external_ref2": forms.TextInput(attrs={"class": "form-control"}),
            "external_ref3": forms.TextInput(attrs={"class": "form-control"}),
            "industry": forms.Select(attrs={"class": "form-control"}),
            "emailOptIn": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "annual_revenue": forms.NumberInput(attrs={"class": "form-control"}),
            "nbr_of_employees": forms.NumberInput(attrs={"class": "form-control"}),
            "currency": forms.Select(attrs={"class": "form-control"}),
            "preferred_communication_language": forms.Select(
                attrs={"class": "form-control"}
            ),
        }

    def clean_work_org_name(self):
        # update field validations here..
        data = self.cleaned_data.get("work_org_name")
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data

    def clean_work_address_line1(self):
        # update field validations here..
        data = self.cleaned_data.get("work_address1")
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data

    def clean_work_address_line2(self):
        data = self.cleaned_data("work_address2")
        return data

    def clean_work_address_line3(self):
        data = self.cleaned_data("work_address3")
        return data

    def clean_work_address_line4(self):
        data = self.cleaned_data("work_address4")
        return data

    def clean_work_address_postcode(self):
        data = self.cleaned_data.get("work_address_postcode")
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        user_org = kwargs.pop("user_org", None)
        super(LeadModelForm, self).__init__(*args, **kwargs)
        users_in_org = User.objects.none()
        users_in_org = User.objects.filter(userorganization=user_org)
        category_in_org = Category.objects.none()
        category_in_org = Category.objects.filter(organisation=user_org)

        self.fields["assigned_to"].queryset = users_in_org
        self.fields["status"].queryset = category_in_org
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    "Personal Information",
                    HTML(
                        """

                    <div class="row">
                        <div class="col-sm-3">
                          <div class="card">
                            <div class="text-center">
                                {% if form.profile_picture.value %}
                                    <img class="center" src= "{{ MEDIA_URL }}{{ form.profile_picture.value }}" width ="250" height="250" alt="Profile Image"  >
                                {% else %}
                                    <p>No Image</p>
                                {% endif %}
                            </div>
                            <div class="card-body">
                                <h5 class="card-title">Profile Picture</h5>
                                <div class="small font-italic text-muted mb-4">JPG or PNG no larger than 5 MB</div>
                            </div>
                          </div>
                        </div>
                        <div class="col-sm-9">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Personal Information</h5>

                                        <div class="form-row">
                                            <div class="form-group col-md-2">
                                                <label for="id_title">Title</label>
                                                {{ form.title }}
                                            </div>
                                            <div class="form-group col-md-4">
                                                <label for="inputfname">First Name</label>
                                                {{form.first_name}}
                                            </div>
                                            <div class="form-group col-md-4">
                                                <label for="inputlname">Last Name</label>
                                                {{form.last_name}}
                                            </div>
                                        </div>
                                        <div class="form-row">
                                            <div class="form-group col-md-4">
                                                <label for="inputdob">Date of Birth</label>
                                                {{form.date_of_birth}}
                                            </div>
                                            <div class="form-group col-md-2">
                                                <label for="inputage">Age</label>
                                                {{form.age}}
                                            </div>
                                        </div>
                                        <div class="form-row">
                                            <div class="form-group col-md-9">
                                                <label for="id_profile_picture">Profile Image - </label>
                                                {{ form.profile_picture }}
                                            </div>
                                        </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    ),
                ),
                Tab(
                    "Company Data",
                    HTML(
                        """
                    <div class="col-sm-12">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Work Information</h5>

                                <div class="form-row">
                                    <div class="form-group col-md-12">
                                        <label for="inputorg">Company Name</label>
                                        {{form.work_org_name}}
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="form-group col-md-6">
                                        <label for="inputwaddress1">Address Line 1</label>
                                        {{form.work_address1}}
                                    </div>
                                    <div class="form-group col-md-6">
                                        <label for="inputwaddress2">Address Line 2</label>
                                        {{form.work_address2}}
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="form-group col-md-6">
                                        <label for="inputwaddress3">Address Line 3</label>
                                        {{form.work_address3}}
                                    </div>
                                    <div class="form-group col-md-6">
                                        <label for="inputwaddress4">Address Line 4</label>
                                        {{form.work_address4}}
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="form-group col-md-3">
                                        <label for="inputwork_address_city">City</label>
                                        {{form.work_address_city}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwork_address_state_county">State/County</label>
                                        {{form.work_address_state_county}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwork_address_postcode">Postcode/Zipcode</label>
                                        {{form.work_address_postcode}}
                                    </div>
                                    <div class="form-group col-md-3">
                                        <label for="inputwork_address_country">Country</label>
                                        {{form.work_address_country}}
                                    </div>
                                </div>
                                <hr>
                                <div class="form-row">
                                    <div class="form-group col-md-3">
                                        <label for="inputwork_Role">Work Role</label>
                                        {{form.work_Role}}
                                    </div>
                                    <div class="form-group col-md-9">
                                        <label for="inputwebsite">Website</label>
                                        {{form.website}}
                                    </div>
                                    <div class="form-group col-md-4">
                                        <label for="inputindustry">Industry</label>
                                        {{form.industry}}
                                    </div>
                                    <div class="form-group col-md-4">
                                        <label for="inputannual_revenue">Annual Revenue</label>
                                        {{form.annual_revenue}}
                                    </div>
                                    <div class="form-group col-md-2">
                                        <label for="inputannual_revenue">Currency</label>
                                        {{form.currency}}
                                    </div>
                                    <div class="form-group col-md-2">
                                        <label for="inputnbr_of_employees">Number of Employees</label>
                                        {{form.nbr_of_employees}}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    ),
                ),
                Tab(
                    "Contact Information",
                    HTML(
                        """
                    <div class="col-sm-12">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Contact Information </h5>

                                    <div class="form-row">
                                        <div class="form-group col-md-8">
                                            <label for="inputemail">Email</label>
                                            {{form.email}}
                                        </div>
                                        <div class="form-group col-md-4">
                                            <div class="form-check">
                                                {{ form.emailOptIn }}
                                                <label class="form-check-label" for="id_emailOptIn"> Email Marketing Opt In </label>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-row">
                                        <div class="form-group col-md-6">
                                            <label for="inputphone_number"> Phone Number</label>
                                            {{form.phone_number}}
                                        </div>
                                        <div class="form-group col-md-6">
                                            <label for="inputmobile_number">Mobile Number</label>
                                            {{form.mobile_number}}
                                        </div>
                                        <div class="form-group col-md-6">
                                            <label for="inputpreferred_contact_preference"> Contact Method Preference</label>
                                            {{form.preferred_contact_preference}}
                                        </div>
                                        <div class="form-group col-md-6">
                                            <label for="inputpreferred_contact_time">Contact Time Preference</label>
                                            {{form.preferred_contact_time}}
                                        </div>
                                        <div class="form-group col-md-6">
                                            <label for="inputpreferred_contact_time">Preferred Language</label>
                                            {{form.preferred_communication_language}}
                                        </div>
                                    </div>
                                    <div class="form-row">
                                        <div class="form-group col-md-9">
                                            <label for="inputsecondary_email">Secondary Email</label>
                                            {{form.secondary_email}}
                                        </div>
                                        <div class="form-group col-md-9">
                                            <label for="inputsocial_media_1">Social Media Profile Link 1 </label>
                                            {{form.social_media_1}}
                                        </div>
                                        <div class="form-group col-md-9">
                                            <label for="inputsocial_media_2">Social Media Profile Link 2</label>
                                            {{form.social_media_2}}
                                        </div>
                                        <div class="form-group col-md-9">
                                            <label for="inputsocial_media_3">Social Media Profile Link 3</label>
                                            {{form.social_media_3}}
                                        </div>
                                    </div>
                            </div>
                        </div>
                    </div>
                    """,
                    ),
                ),
                Tab(
                    "Manage Lead",
                    HTML(
                        """
                    <div class="col-sm-12">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Lead Status</h5>

                                    <div class="form-row">
                                        <div class="form-group col-md-4">
                                            <label for="inputteam">Assigned to Team</label>
                                            {{form.team}}
                                        </div>
                                        <div class="form-group col-md-4">
                                            <label for="inputassigned_to">Assigned Agent</label>
                                            {{form.assigned_to}}
                                        </div>
                                        <div class="form-group col-md-4">
                                            <label for="inputstatus">Status</label>
                                            {{form.status}}
                                        </div>
                                        <div class="form-group col-md-4">
                                            <label for="inputsource">Source</label>
                                            {{form.source}}
                                        </div>
                                        <div class="form-group col-md-4">
                                            <label for="inputlead_Ratings">Lead Rating</label>
                                            {{form.lead_Ratings}}
                                        </div>
                                    </div>
                                    <div class="form-row">
                                        <div class="form-group col-md-12">
                                            <label for="inputdescription">Description</label>
                                            {{form.description}}
                                        </div>
                                        <div class="form-group col-md-12">
                                            <label for="inputcloseReason">Close Reason</label>
                                            {{form.closeReason}}
                                        </div>
                                    </div>

                            </div>
                        </div>
                    </div>
                    """,
                    ),
                ),
                Tab(
                    "Additional Information",
                    HTML(
                        """
                    <div class="col-sm-12">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">External referrences</h5>

                                <div class="form-row">
                                    <div class="form-group col-md-12">
                                        <label for="inputexternal_ref1">External Reference 1</label>
                                        {{form.external_ref1}}
                                    </div>
                                    <div class="form-group col-md-12">
                                        <label for="inputexternal_ref2">External Reference 2 </label>
                                        {{form.external_ref2}}
                                    </div>
                                    <div class="form-group col-md-12">
                                        <label for="inputexternal_ref3">External Reference 3 </label>
                                        {{form.external_ref3}}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    ),
                ),
            )
        )
        self.helper.layout.append(
            Submit("submit", "Update Lead"),
        )


class NoteModelForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            "title",
            "notes",
            "file",
        ]
        exclude = [
            "dateTimeModified",
            "dateTimeCreated",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "cols": 45, "rows": 10}
            ),
            "file": forms.widgets.ClearableFileInput(
                attrs={"class": "form-control-file", "cols": 45, "rows": 10}
            ),
        }

    def clean_content(self):
        # update field validations here..
        data = self.cleaned_data.get("notes")
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data
