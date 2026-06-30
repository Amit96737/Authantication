from django import forms
from bank.models.bank import BankName
from bank.models.account import BankAccount

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ("customer_name", "phone_number", "email", "gender", "bank", "address", "aadhar_number")

        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'bank': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BankNameForm(forms.ModelForm):
    class Meta:
        model = BankName
        fields = ("name", )