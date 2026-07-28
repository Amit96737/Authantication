from django import forms
from payments.models.product import Item
from tinymce.widgets import TinyMCE

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'brand', 'price', 'mrp', 'quantity', 'colors', 'size', 'category', 'description', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'mrp': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'colors': forms.TextInput(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': TinyMCE(attrs={'class': 'form-control'}),
        }