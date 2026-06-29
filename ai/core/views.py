from django.shortcuts import render

def chat_about_page(request):
    return render(request, "chat/chat_about_page.html", locals())

def chat_boat_home(request):
    return render(request, "chat/chatboat.html")

def master_chef_home(request):
    return render(request, "chat/master_chef_home.html")