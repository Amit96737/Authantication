from django import forms
from django.core.validators import FileExtensionValidator
from users.models.users import User
import re
from django.core.exceptions import ValidationError

gender_choices = (
    ('', 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
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
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )
    profile_pic = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])],
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a strong password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a strong password'
        })
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least 1 uppercase letter")

        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least 1 lowercase letter")

        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least 1 number")

        if not re.search(r'[!@#$%^&*]', password):
            raise ValidationError("Password must contain at least 1 special character")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Password and Confirm Password do not match")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'biograph',
            'profile_pic'
        ]

        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }