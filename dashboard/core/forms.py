from django import forms
from django.core.validators import FileExtensionValidator

gender_choices = (
    ('', 'Select Gender'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others'),
)

class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
    )
    last_name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
    )
    gender = forms.ChoiceField(
        choices=gender_choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'})
    )
    phone_number = forms.CharField(
        max_length=13, min_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91XXXXXXXXXX'})
    )
    profile_pic = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])],
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a strong password'
        })
    )

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )