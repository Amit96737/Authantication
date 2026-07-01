from django.shortcuts import render
from bank.core.forms import BankAccountForm, BankNameForm
from bank.models.account import BankAccount
from django.contrib import messages
from django.shortcuts import redirect
from bank.core.services import send_account_email
from bank.models.bank import BankName
from bank.core.forms import DepositForm
from bank.core.services import send_deposit_email,send_withdraw_email

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

def deposit(request):
    if request.method == "POST":
        form = DepositForm(request.POST, type="deposit")
        if form.is_valid():
            account_number = form.cleaned_data["account_number"]
            amount = form.cleaned_data["amount"]

            try:
                account = BankAccount.objects.get(account_number=account_number)
                if amount <= 0:
                    messages.error(request, "Amount must be greater than zero")
                    return redirect("deposit_amount")

                account.balance += amount
                account.save()

                send_deposit_email(account, amount)

                messages.success(request, f"+₹{amount} deposited successfully")
                return redirect("deposit_amount")

            except BankAccount.DoesNotExist:
                messages.error(request, "Account not found")

    else:
        form = DepositForm()

    return render(request, "bank/deposit.html", {"form": form})

def withdraw(request):
    if request.method == "POST":
        form = DepositForm(request.POST, type="withdraw")

        if form.is_valid():
            account_number = form.cleaned_data["account_number"]
            amount = form.cleaned_data["amount"]

            account = BankAccount.objects.get(account_number=account_number)

            account.balance -= amount
            account.save()

            send_withdraw_email(account, amount)

            messages.success(request, f"-₹{amount} withdrawn successfully")
            return redirect("withdraw_amount")

    else:
        form = DepositForm()

    return render(request, "bank/withdraw.html", {"form": form})


def check_balance(request):
    balance = None
    account_number = ""
    ifsc_code = ""

    if request.method == "POST":
        account_number = request.POST.get("account_number")
        ifsc_code = request.POST.get("ifsc_code")

        try:
            account = BankAccount.objects.get(account_number=account_number)

            if not account.account_status:
                messages.error(request, "Please activate your account first")

            elif account.bank.ifsc_code != ifsc_code:
                messages.error(request, "Invalid IFSC Code")

            else:
                balance = account.balance

        except BankAccount.DoesNotExist:
            messages.error(request, "Account not found")

    return render(request, "bank/check_balance.html", {
        "balance": balance,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
    })

def specific_account(request):
    account = None
    account_number = ""
    ifsc_code = ""

    if request.method == "POST":
        account_number = request.POST.get("account_number")
        ifsc_code = request.POST.get("ifsc_code")

        try:
            account = BankAccount.objects.get(account_number=account_number)

            if account.bank.ifsc_code != ifsc_code:
                messages.error(request, "Invalid IFSC Code")

                account = None

        except BankAccount.DoesNotExist:
            messages.error(request, "Account not found")

    return render(request, "bank/specific_account.html", {
        "account": account,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
    })