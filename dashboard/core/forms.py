from django import forms
from django.core.validators import FileExtensionValidator
from users.models.users import User

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

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'profile_pic', 'biograph']
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'First Name'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Last Name'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Email Address'}),
#             'phone_number': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Phone Number'}),
#             'gender': forms.Select(attrs={'class': 'form-select rounded-3'}),
#             'profile_pic': forms.FileInput(attrs={'class': 'form-control rounded-3'}),
#             'biograph': forms.Textarea(
#                 attrs={'class': 'form-control rounded-3', 'rows': 4, 'placeholder': 'Tell us about yourself...'}),
#
#         }