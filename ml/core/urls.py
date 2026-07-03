from django.urls import path
from . import views

urlpatterns = [
    path('salary/', views.salary_form, name='salary_form'),
    path('predict/', views.predict_salary, name='predict_salary'),
]

