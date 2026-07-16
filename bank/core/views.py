from twilio.rest.ip_messaging.v1.service import user

from django.shortcuts import render
from bank.core.forms import BankAccountForm, BankNameForm, IdentificationForm
from bank.models.account import BankAccount
from django.contrib import messages
from django.shortcuts import redirect
from bank.core.services import send_account_email
from bank.models.bank import BankName
from bank.core.forms import DepositForm
from bank.core.services import send_deposit_email, send_withdraw_email, send_transfer_email
from decimal import Decimal
from bank.models.transaction import Transaction
from bank.models.identity_verification import Identification


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

            request.session['bank_account_id'] = str(account.id)

            try:
                send_account_email(account)

            except Exception as e:
                print(f"Email error: {e}")
                messages.warning(request, "Account created, but we faced an issue sending the verification email.")

            messages.success(request, "Account created successfully. First Upload document details")
            return redirect('identity_verification')
    else:
        form = BankAccountForm()

    return render(request, "bank/create_account.html", {'form': form})

def activate_account(request, id):
    account = BankAccount.objects.get(id=id)
    account.account_status = True
    account.save()
    return render(
        request,
        "bank/notification_home.html",
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
                if not account.account_status:
                    messages.error(request, "Please activate your account first")
                    return redirect("deposit_amount")

                if amount <= 0:
                    messages.error(request, "Amount must be greater than zero")
                    return redirect("deposit_amount")

                account.balance += amount
                account.save()

                Transaction.objects.create(
                    receiver=account,
                    transaction_type="DEPOSIT",
                    amount=amount,
                    balance_after_transaction=account.balance
                )

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
            if not account.account_status:
                messages.error(request, "Please activate your account first")
                return redirect("withdraw_amount")

            account.balance -= amount
            account.save()

            Transaction.objects.create(
                sender=account,
                transaction_type="WITHDRAW",
                amount=amount,
                balance_after_transaction=account.balance
            )

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

def transfer_amount(request):
    sender_acc = ""
    sender_ifsc = ""
    receiver_acc = ""
    receiver_ifsc = ""
    amount = ""
    if request.method == "POST":
        sender_acc = request.POST.get("sender_account")
        sender_ifsc = request.POST.get("sender_ifsc")

        receiver_acc = request.POST.get("receiver_account")
        receiver_ifsc = request.POST.get("receiver_ifsc")

        amount = Decimal(request.POST.get("amount"))

        try:
            sender = BankAccount.objects.get(account_number=sender_acc)
            receiver = BankAccount.objects.get(account_number=receiver_acc)

            if not sender.account_status:
                messages.error(request, "Activate your account first")

            elif not receiver.account_status:
                messages.error(request, "Receiver account inactive")

            elif sender.bank.ifsc_code != sender_ifsc:
                messages.error(request, "Invalid sender IFSC")

            elif receiver.bank.ifsc_code != receiver_ifsc:
                messages.error(request, "Invalid receiver IFSC")

            elif sender.balance < amount:
                messages.error(request, "Insufficient balance")

            else:
                sender.balance -= amount
                receiver.balance += amount

                sender.save()
                receiver.save()

                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    transaction_type="TRANSFER",
                    amount=amount,
                    balance_after_transaction=sender.balance
                )

                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    transaction_type="TRANSFER",
                    amount=amount,
                    balance_after_transaction=receiver.balance
                )

                send_transfer_email(sender, receiver, amount)

                messages.success(request, "Transfer successful")
                sender_acc = sender_ifsc = receiver_acc = receiver_ifsc = amount = ""

        except BankAccount.DoesNotExist:
            messages.error(request, "Account not found")

    return render(request, "bank/transfer_amount.html",
                  {
                      "sender_account": sender_acc,
                      "sender_ifsc": sender_ifsc,
                      "receiver_account": receiver_acc,
                      "receiver_ifsc": receiver_ifsc,
                      "amount": amount,
                  }
                  )

def transaction_history(request):
    account = None
    transactions = None
    account_number = ""
    ifsc_code = ""

    if request.method == "POST":
        account_number = request.POST.get("account_number")
        ifsc_code = request.POST.get("ifsc_code")

        try:
            account = BankAccount.objects.get(account_number=account_number)

            if not account.account_status:
                messages.error(request, "Activate your account first")

            elif account.bank.ifsc_code != ifsc_code:
                messages.error(request, "Invalid IFSC Code")

            else:
                from django.db.models import Q

                transactions = Transaction.objects.filter(
                    Q(sender=account) | Q(receiver=account)
                ).order_by('-created_at')

        except BankAccount.DoesNotExist:
            messages.error(request, "Account not found")

    return render(request, "bank/transaction_history.html", {
        "transactions": transactions,
        "account_number": account_number,
        "ifsc_code": ifsc_code,
    })

def identity_verification(request):
    if request.method == "POST":
        form = IdentificationForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data

            bank_user_id = request.session.get('bank_account_id')

            if not bank_user_id:
                messages.error(request, "Session expired")
                return redirect("create_account")

            bank_user = BankAccount.objects.get(id=bank_user_id)

            user = Identification.objects.create(
                customer=bank_user,
                middle_mark_sheet=data['middle_mark_sheet'],
                secondary_mark_sheet=data['secondary_mark_sheet'],
                aadhar_image=data['aadhar_image'],
                pan_card=data['pan_card'],
                verification_status=False
            )
            details=user.save()

        # send_account_email(details)

            messages.success(request, "Please wait document under progress when document verify successfully notify you")
            return redirect("identity_verification")

    else:
        form = IdentificationForm()

    return render(request, "bank/identity_verification.html", locals())