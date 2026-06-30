from django.shortcuts import render
from bank.core.forms import BankAccountForm, BankNameForm
from bank.models.account import BankAccount
from django.contrib import messages
from django.shortcuts import redirect
from bank.core.services import send_account_email
from bank.models.bank import BankName

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
    if request.method == "POST":
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account=form.save()

            try:
                send_account_email(account)

            except Exception as e:
                print(f"Email error: {e}")
                messages.warning(request, "Account created, but we faced an issue sending the verification email.")

            messages.success(request, "Account created successfully. First verify your account check email")
            return redirect('create_account')
    else:
        form = BankAccountForm()

    return render(request, "bank/create_account.html", {'form': form})

def activate_account(request, id):
    account = BankAccount.objects.get(id=id)
    account.account_status = True
    account.save()
    return render(
        request,
        "bank/home.html",
        locals()
    )

def deactivate_account(request, id):
    account = BankAccount.objects.get(id=id)
    account.account_status = False
    account.save()
    return render(request, "bank/create_account.html", locals())

def all_records(request):
    all_accounts = BankAccount.objects.filter(account_status=True).order_by('-id')
    return render(
        request,
        "bank/all_records.html",
        locals()
    )

def create_bank(request):
    if request.method == "POST":
        form = BankNameForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bank Add successfully.")
            return redirect('create_bank')
    else:
        form = BankNameForm()

    return render(request, "bank/create_bank.html", {'form': form})

def all_banks(request):
    all_banks = BankName.objects.all().order_by('-id')
    return render(
        request,
        "bank/all_banks.html",
        locals()
    )