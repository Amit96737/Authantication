from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.sub_admin_dashboard, name="sub_admin_dashboard"),
]