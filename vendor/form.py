from .models import Vendor, OpeningHour
from django import forms
from account.validators import image_upload_validators

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[image_upload_validators])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
        
        
class OpenHoursForm(forms.ModelForm):
    class Meta :
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
        
