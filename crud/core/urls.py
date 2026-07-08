from django.urls import path
from . import views

urlpatterns = [
    path('crud-home-page/', views.crud_home_page, name="crud_home_page"),
    path("create-student/", views.create_student, name="create_student"),
    path('verify-account/<uuid:student_id>/', views.verify_student_account, name="verify_student_account"),
    path('student-details/<uuid:student_id>/', views.student_details, name="student_details"),
    path('update-student-profile/', views.update_student_profile, name="update_student_profile"),
    path('student-delete/<uuid:student_id>/', views.delete_student, name="delete_student"),
    path('student-list/', views.student_list, name="student_list"),
]

