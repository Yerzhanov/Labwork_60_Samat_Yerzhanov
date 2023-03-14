from django import forms
from orders.models import Order

class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Аттрактор'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Скул'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'attractor@example.kz'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'г. Алматы, ул.Жибек Жолы, д.135, блок 3, этаж 8'}))
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')