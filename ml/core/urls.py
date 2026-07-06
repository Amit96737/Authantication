from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.ml_about_page, name='ml_about_page'),
    path('salary/', views.salary_form, name='salary_form'),
    path('predict/', views.predict_salary, name='predict_salary'),
]

