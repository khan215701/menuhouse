from .models import Category
from django import forms
class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'description')