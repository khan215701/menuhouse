from django import forms
from .models import User, profile
from .validators import image_upload_validators

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())
  confirm_password = forms.CharField(widget=forms.PasswordInput())
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']
    
  def clean(self):
    cleaned_data = super(UserForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    
    if password != confirm_password:
      raise forms.ValidationError(
        'Password does not match'
      )
      

class profileForm(forms.ModelForm):
  address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing...', 'required': 'required'}))
  profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[image_upload_validators])
  cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[image_upload_validators])
  class Meta:
    model = profile
    fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'longitude', 'latitude']
    
  def __init__(self, *args, **kwargs):
    super(profileForm, self).__init__(*args, **kwargs)
    for field in self.fields:
      if field == 'longitude' or field == 'latitude':
        self.fields[field].widget.attrs['readable'] = 'readable'
          
      
    
  