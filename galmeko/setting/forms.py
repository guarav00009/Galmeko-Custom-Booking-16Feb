from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from setting.models import Vehicle,VehicleCategory,Features
from user.models import User

class CustomVehicleCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendor'].choices= [(vendor.id, vendor.first_name + ' ' + vendor.last_name) for vendor in User.objects.filter(type = 2)]
    class Meta:
        model = Vehicle
        fields = ('vendor','vehicle_no','mileage','chassis_no','status','vehicle_category')
        widgets = {
            'vehicle_no': forms.TextInput(attrs={'class': 'vTextField form-control','placeholder': 'Vehicle No'}),
            'mileage': forms.TextInput(attrs={'class': 'vTextField form-control','placeholder': 'Mileage'}),
            'chassis_no': forms.TextInput(attrs={'class': 'vTextField form-control','placeholder': 'Chassis No'}),
            'status' : forms.Select(attrs={'class':'vTextField form-control'}),
            'vehicle_category' : forms.Select(attrs={'class':'vTextField form-control'}),
        }  
        error_messages = {
            'vehicle_no': {
                'required': "Vehicle no is required",
            },
            'mileage' : {
                 'required': "Mileage is required",
            },
            'chassis_no' : {
                 'required': "Chassis No is required",
            }
        } 

class CustomCategoryCreationForm(forms.ModelForm):

    class Meta:
        model = VehicleCategory
        fields = ('category_name','status',)

class CustomFeaturesCreationForm(forms.ModelForm):

    class Meta:
        model = Features
        fields = ('name','status',)
