from django import forms

from .models import TeamMembership,Team
from django.contrib.auth import get_user_model

User = get_user_model()

class MembershipForm(forms.ModelForm):
    def __init__(self,organisation,*args,**kwargs):
        super (MembershipForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['team'].queryset = Team.objects.filter(organisation=organisation)
        self.fields['member'].queryset = User.objects.filter(userorganization=organisation)

    class Meta:
        model = TeamMembership
        fields = [
            'team',
            'member',
            'role',
        ]
        exclude = [
            'slug',
            'dateTimeModified',
            'dateTimeCreated',
        ],
        autocomplete_fields=['member']
        widgets = {
            'team': forms.Select(attrs={'class':'form-control'}),
            'member': forms.Select(attrs={'class':'form-control'}),
            'role': forms.Select(attrs={'class':'form-control'}),

        }

# class MembershipForm(forms.Form):
#     member = forms.ChoiceField(fieldchoices= ,
#     required=True,
#     widget=forms.Select(attrs={'class':'form-control'}),
#     )
# class TeamMembershipModelForm(forms.ModelForm):
#     class Meta:
#         model = TeamMembership
#         fields = [
#             'team',
#             'users_in_same_org',
#             'role',
#         ]
#         exclude = [
#             'slug',
#             'dateTimeModified',
#             'dateTimeCreated',
#         ],
#         autocomplete_fields=['member']
#         widgets = {
#             'team': forms.Select(attrs={'class':'form-control'}),
#             'users_in_same_org': forms.Select(attrs={'class':'form-control'}),
#             'role': forms.Select(attrs={'class':'form-control'}),

#         }

#     def clean_content(self):
#         # update field validations here..
#         data = self.cleaned_data.get('team')
#         if len(data) <= 0:
#             raise forms.ValidationError("This field is required")
#         return data