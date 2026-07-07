from django.shortcuts import render

def home(request):
    return render(request, "notification/notification_home.html", locals())

def about(request):
    return render(request, "notification/notification_about.html", locals())