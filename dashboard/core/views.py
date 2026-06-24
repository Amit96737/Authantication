from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from users.models.users import User
from users.services.send_otp_verification import send_otp_to_mail, send_otp_to_phone
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.core.cache import cache

def dashboard(request):
    return render(
        request,
        "dashboard/dashboard.html",
        locals()
    )

def user_sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            user=User.objects.create_user(
                username=data['first_name'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                gender=data['gender'],
                email=data['email'],
                phone_number=data['phone_number'],
                profile_pic=data['profile_pic'],
                password=data['password']
            )

            if user and not user.email_verified:
                full_name = f"{user.first_name}"

                send_otp_to_mail(
                    username=full_name,
                    user_email=user.email.lower()
                )

                messages.success(request, "OTP sent to your email. Please verify your account.")
                return redirect(f"/verify-email-otp/?email={user.email}")
    else:
        form = SignUpForm()

    return render(
        request,
        "dashboard/users.html",
        {'form': form}
    )


def verify_email_otp(request):
    email = request.GET.get('email')

    if not email:
        messages.error(request, "Invalid request. Please sign up again.")
        return redirect('user_sign_up')

    if request.method == "POST":
        otp_digits = [
            request.POST.get('otp_1', ''),
            request.POST.get('otp_2', ''),
            request.POST.get('otp_3', ''),
            request.POST.get('otp_4', ''),
            request.POST.get('otp_5', ''),
            request.POST.get('otp_6', '')
        ]
        user_otp = "".join(otp_digits)

        cache_key = f"otp_{email.lower()}"
        saved_otp = cache.get(cache_key)

        user = User.objects.filter(email=email).first()

        if user:
            if saved_otp and str(user_otp) == str(saved_otp):
                user.email_verified = True
                user.save()

                cache.delete(cache_key)

                send_otp_to_phone(username=user.first_name, phone_number=user.phone_number)

                messages.success(request, "Email verified successfully! Now enter the OTP sent to your phone.")
                return redirect(f"/verify-sms-otp/?email={user.email}&phone={user.phone_number}")
            else:
                messages.error(request, "Invalid OTP code. Please try again.")
        else:
            messages.error(request, "User not found.")

    return render(request, "dashboard/email_verify.html", {'email': email})


def verify_sms_otp(request):
    email = request.GET.get('email')
    raw_phone = request.GET.get('phone')

    if not email or not raw_phone:
        messages.error(request, "Verification session broken. Please sign up again.")
        return redirect('user_sign_up')

    phone = raw_phone.strip().replace(" ", "+")

    if not phone.startswith('+'):
        phone = f"+{phone}"

    if request.method == "POST":
        otp_digits = [
            request.POST.get('otp_1', ''),
            request.POST.get('otp_2', ''),
            request.POST.get('otp_3', ''),
            request.POST.get('otp_4', ''),
            request.POST.get('otp_5', ''),
            request.POST.get('otp_6', '')
        ]
        user_otp = "".join(otp_digits)

        cache_key = f"sms_otp_{phone}"
        saved_otp = cache.get(cache_key)

        user = User.objects.filter(email=email.lower()).first()

        if user:
            if saved_otp and str(user_otp) == str(saved_otp):
                cache.delete(cache_key)
                messages.success(request, "Phone number verified successfully! You can now log in.")
                return redirect('user_login')
            else:
                messages.error(request, "Invalid or expired SMS OTP code. Please try again.")
        else:
            messages.error(request, "User identity verification failed.")

    return render(request, "dashboard/sms_verify.html", {'phone': phone})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']

            user = User.objects.filter(email=email).first()

            if user:
                if check_password(password, user.password):

                    if not user.email_verified:
                        request.session['signup_email'] = user.email.lower()
                        messages.warning(request, "Please verify your email before logging in.")
                        return redirect('verify_email_otp')

                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid Password. Please try again.")
            else:
                messages.error(request, "No account found with this email.")
    else:
        form = LoginForm()

    return render(
        request,
        "dashboard/login.html",
        {'form': form}
    )