from django import forms
from .models import Product, ProductCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'quantity', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description']

class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти товар")
