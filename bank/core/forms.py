from django import forms
from bank.models.bank import BankName
from bank.models.account import BankAccount

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ("customer_name", "phone_number", "email", "gender", "bank", "address", "aadhar_number")

        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control',"placeholder": "+91776756564"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', "placeholder": "example@gmail.com"}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'bank': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control', "placeholder": "878767676767"}),
        }

class BankNameForm(forms.ModelForm):
    class Meta:
        model = BankName
        fields = ("name", )

# DepositForm Same form use as Withdraw Money case

class DepositForm(forms.Form):
    account_number = forms.CharField(max_length=9, min_length=9,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "maxlength": "9",
            "pattern": "[0-9]{9}",
            "placeholder": "Enter 9 digit account number"
        })
    )
    ifsc_code = forms.CharField(max_length=11, min_length=11,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "maxlength": "11",
            "placeholder": "Enter IFSC Code"
        })
    )
    amount = forms.DecimalField(max_digits=20, decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "step": "0.01"
        })
    )

    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop("type", None)
        super().__init__(*args, **kwargs)

    def clean_account_number(self):
        account_number = self.cleaned_data.get("account_number")
        if not account_number.isdigit():
            raise forms.ValidationError("Account number must be numeric")
        return account_number

    def clean(self):
        cleaned_data = super().clean()
        account_number = cleaned_data.get("account_number")
        ifsc_code = cleaned_data.get("ifsc_code")
        amount = cleaned_data.get("amount")

        if not account_number:
            return cleaned_data

        try:
            account = BankAccount.objects.get(account_number=account_number)

        except BankAccount.DoesNotExist:
            raise forms.ValidationError("Account not found")

        if not account.account_status:
            raise forms.ValidationError(
                "Please activate your account via email verification"
            )

        if ifsc_code and account.bank.ifsc_code != ifsc_code:
            raise forms.ValidationError("Invalid IFSC Code for this account")

        if amount is not None:
            if amount <= 0:
                raise forms.ValidationError("Amount must be greater than zero")

            if self.type == "withdraw":
                if account.balance < amount:
                    raise forms.ValidationError("Insufficient balance")

        return cleaned_data

