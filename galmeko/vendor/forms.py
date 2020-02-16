from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from vendor.models import Vendor,Driver

class CustomVendorCreationForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['company_name',]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'vTextField form-control','placeholder': 'Company Name'}),
        } 


class CustomDriverCreationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name','last_name','email','image','address','phone',]