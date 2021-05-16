from django import forms

from .models import PaymentMethod

class PaymentMethodModelForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = [
            'expiry_month',
            'expiry_year',
        ]
        exclude = [
            'user',
            'subscription',
            'stripe_payment_method_id'
            'type',
            'country',
            'fingerprint',
            'cardId',
            'is_default'
            'dateTimeModified'
            'dateTimeCreated'

        ]
        widgets = {
            'expiry_month': forms.Select(attrs={'class':'form-control'}),
            'expiry_year': forms.Select(attrs={'class':'form-control'}),
        }
    def clean_content(self):
        # update field validations here..
        data = self.cleaned_data.get('bond_type')
        if len(data) <= 0:
            raise forms.ValidationError("This field is required")
        return data