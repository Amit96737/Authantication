from django import forms
from crud.models.student import Student

class StudentForm(forms.ModelForm):
    address = forms.TextInput()
    biograph = forms.CharField(max_length=255)
    class Meta:
        model = Student
        fields = ("first_name", "last_name", "email", "phone_number", "gender", "profile_pic", "address", "biograph")

class UpdateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'gender',
            'biograph',
            'profile_pic'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'biograph': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }