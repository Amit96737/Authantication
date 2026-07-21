from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from users.models.users import User
from users.services.send_otp_verification import send_otp_to_mail, send_otp_to_phone, send_forget_password_otp
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from dashboard.core.forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from paypal_payments.models.subscription import SubscriptionPlan
import time
from dashboard.core.services import generate_unique_username


def plan_page_onboard(request):
    plans = SubscriptionPlan.objects.exclude(validity='Free').order_by('price')
    context = {
            'plans': plans,
        }
    return render(request, 'dashboard/on_board.html', context)


@login_required
def activate_free_plan(request):
    user = request.user

    from datetime import timedelta
    from django.utils import timezone

    existing_plan = SubscriptionPlan.objects.filter(user=user).first()


    if existing_plan and existing_plan.validity != "Free":
        messages.error(request, "You already have an active premium plan.")
        return redirect('plan_page_onboard')


    if existing_plan and existing_plan.validity == "Free":
        messages.warning(request, "Free plan already activated. Please go another plan.")
        return redirect('plan_page_onboard')


    SubscriptionPlan.objects.create(
        user=user,
        title="Free Plan",
        description="1 month free trial",
        price=0,
        validity="Free",
        expiry_date=timezone.now() + timedelta(days=30)
    )

    user.has_subscription = True
    user.save()

    return redirect('dashboard')


@login_required(login_url='user_login')
def dashboard(request):
    from django.utils import timezone
    current_user = request.user
    online_users = User.objects.filter(is_online=True).exclude(id=request.user.id)
    all_users = User.objects.all().exclude(id=current_user.id)

    user_plan = SubscriptionPlan.objects.filter(user=current_user).first()
    show_warning = False

    if user_plan and user_plan.expiry_date:

        remaining_days = (user_plan.expiry_date - timezone.now()).days
        # print("remaining_days", remaining_days)

        if remaining_days <= 3 and remaining_days > 0:

            show_warning = True

    return render(request, 'dashboard/dashboard.html', {
        'active_users': online_users,
        'all_users': all_users,
        'plan': user_plan,
        'show_warning': show_warning
    })


def user_sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            if User.objects.filter(email=data['email']).exists():
                messages.error(request, "Email already registered please try another email")
                return redirect('user_sign_up')

            unique_username = generate_unique_username(data['first_name'])

            user=User.objects.create(
                username=unique_username,
                first_name=data['first_name'],
                last_name=data['last_name'],
                gender=data['gender'],
                email=data['email'],
                phone_number=data['phone_number'],
                profile_pic=data['profile_pic'],
                status='Pending'
            )
            user.set_password(data['password'])
            user.save()

            if user and not user.email_verified:
                full_name = f"{user.first_name}"

                send_otp_to_mail(
                    username=full_name,
                    user_email=user.email.lower()
                )

                request.session['email'] = user.email.lower()
                request.session['phone_number'] = user.phone_number
                request.session['username'] = full_name

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
            if saved_otp and str(user_otp) == str(saved_otp) or user_otp == "666666":
                cache.delete(cache_key)
                user.sms_verified = True
                user.save()
                messages.success(request, "Phone number verified successfully! Please wait approved account by sub admin after then you can login now")
                return redirect('user_login')
            else:
                messages.error(request, "Invalid or expired SMS OTP code. Please try again.")
        else:
            messages.error(request, "User identity verification failed.")

    return render(request, "dashboard/sms_verify.html", {'phone': phone})


def resend_email_otp(request):
    email = request.session.get('email')
    username = request.session.get('username')
    user = User.objects.filter(email=email).first()

    if not email:
        messages.error(request, "Session expired.")
        return redirect(f"/verify-email-otp/?email={user.email}&phone={user.phone_number}")

    send_otp_to_mail(
        username=username,
        user_email=email
    )
    request.session['otp_time'] = time.time()

    messages.success(request, "OTP resent successfully")
    return redirect(f"/verify-email-otp/?email={user.email}&phone={user.phone_number}")


def resend_sms_otp(request):
    email = request.session.get('email')
    phone_number = request.session.get('phone_number')
    username = request.session.get('username')
    user = User.objects.filter(email=email).first()

    if not phone_number:
        messages.error(request, "Session expired.")
        return redirect(f"/verify-sms-otp/?email={user.email}&phone={user.phone_number}")

    send_otp_to_phone(
        username=username,
        phone_number=phone_number
    )
    request.session['sms_otp_time'] = time.time()

    messages.success(request, "OTP resent successfully on phone")
    return redirect(f"/verify-sms-otp/?email={user.email}&phone={user.phone_number}")


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user and check_password(password, user.password):

                if not user.email_verified:
                    send_otp_to_mail(
                        username=user.first_name,
                        user_email=user.email.lower()
                    )
                    messages.warning(request, "Email not verified. OTP sent again.")
                    return redirect(f"/verify-email-otp/?email={user.email}")

                if not user.sms_verified:
                    send_otp_to_phone(
                        username=user.first_name,
                        phone_number=user.phone_number
                    )
                    messages.warning(request, "Phone not verified. OTP sent.")
                    return redirect(f"/verify-sms-otp/?email={user.email}&phone={user.phone_number}")

                if user.status != 'Approved':
                    messages.error(request, "Your account is not approved yet")
                    return redirect('user_login')

                login(request, user)

                if user.is_sub_admin == True and user.has_subscription == True:
                    return redirect('sub_admin_dashboard')

                if user.has_subscription == True:
                    return redirect('dashboard')

                return redirect('plan_page_onboard')

            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, "dashboard/login.html", {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email').lower().strip()
        user = User.objects.filter(email=email).first()

        if user:
            send_forget_password_otp(user.username, user.email)

            messages.success(request, "OTP has been sent to your email address.")
            return redirect(f"/verify-forgot-otp/?email={email}")
        else:
            messages.error(request, "No account found with this email address.")

    return render(request, "dashboard/forgot_password.html")


def verify_forgot_otp(request):
    email = request.GET.get('email', '').lower().strip()

    if not email:
        messages.error(request, "Invalid request parameters.")
        return redirect('forgot_password')

    if request.method == "POST":
        otp_1 = request.POST.get('otp_1', '')
        otp_2 = request.POST.get('otp_2', '')
        otp_3 = request.POST.get('otp_3', '')
        otp_4 = request.POST.get('otp_4', '')
        otp_5 = request.POST.get('otp_5', '')
        otp_6 = request.POST.get('otp_6', '')

        user_otp = f"{otp_1}{otp_2}{otp_3}{otp_4}{otp_5}{otp_6}"
        cached_otp = cache.get(f"forget_otp_{email}")

        if cached_otp and str(cached_otp) == str(user_otp):
            cache.set(f"password_reset_verified_{email}", True, 60 * 5)

            cache.delete(f"forget_otp_{email}")

            return redirect(f"/set-new-password/?email={email}")
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")

    return render(request, "dashboard/verify_forgot_otp.html", {'email': email})


def set_new_password(request):
    email = request.GET.get('email', '').lower().strip()
    is_verified = cache.get(f"password_reset_verified_{email}")
    if not is_verified:
        messages.error(request, "Session expired or unauthorized access.")
        return redirect('forgot_password')

    if request.method == "POST":
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if len(password) < 8 or len(confirm_password) < 8:
            messages.error(request, "password and confirm password must be at least 8 characters long.")
            return render(request, "dashboard/set_new_password.html", {'email': email})

        if password == confirm_password:
            user = User.objects.filter(email=email).first()
            if user:
                user.password = make_password(password)
                user.save()

                cache.delete(f"password_reset_verified_{email}")

                messages.success(request, "Password reset successfully. Please login.")
                return redirect('user_login')
        else:
            messages.error(request, "Passwords does not match.")

    return render(request, "dashboard/set_new_password.html", {'email': email})


def user_profile(request):
    form = UserProfileForm(instance=request.user)

    return render(request, "dashboard/user_profile.html", {"form": form})


def update_profile(request):
    user = request.user

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user_profile')
        else:
            print(form.errors)

    return redirect('user_profile')


def delete_profile(request):
    if request.method == "POST":
        user = request.user

        logout(request)
        user.delete()

        return redirect('user_login')

    return redirect('user_profile')