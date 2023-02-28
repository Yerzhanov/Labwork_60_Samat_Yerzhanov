from django.forms import ModelForm
from .models import Product, ProductCategory


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'quantity', 'image']

class CategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name', 'description']
