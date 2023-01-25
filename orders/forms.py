from django import forms
from .models import Order,  OrderedFood
class orderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address', 'country', 'state', 'city', 'pin_code']
        