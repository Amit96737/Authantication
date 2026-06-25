from django import forms
from crud.models.student import Student

class StudentForm(forms.ModelForm):
    address = forms.TextInput()
    biograph = forms.CharField(max_length=255)
    class Meta:
        model = Student
        fields = ("first_name", "last_name", "email", "phone_number", "gender", "profile_pic", "address", "biograph")
