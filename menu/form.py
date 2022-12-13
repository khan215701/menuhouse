from .models import Category, FoodItem
from django import forms
from account.validators import image_upload_validators

class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'description')
        
        
class foodForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}))
    class Meta:
        model = FoodItem
        fields = ['food_title', 'category', 'description', 'price', 'image', 'is_available']