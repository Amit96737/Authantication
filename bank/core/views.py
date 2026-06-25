from django.shortcuts import render

def bank_dashboard(request):
    return render(
        request,
        "bank/home.html",
        locals()
    )