from django.shortcuts import render

def bank_about_page(request):
    return render(
        request,
        "bank/bank_about_page.html",
        locals()
    )


def bank_dashboard(request):
    return render(
        request,
        "bank/home.html",
        locals()
    )

def create_account(request):
    return render(
        request,
        "bank/create_account.html",
        locals()
    )