from django.contrib import admin
from crud.models.student import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'email', 'phone_number', 'gender', 'address', 'biograph')

admin.site.register(Student, StudentAdmin)
