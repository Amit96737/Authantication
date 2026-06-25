from django.shortcuts import redirect
from .forms import StudentForm
from crud.core.services import send_verification_email
from crud.models.student import Student
from django.shortcuts import get_object_or_404, render
from django.contrib import messages

def create_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student=form.save()

            try:
                send_verification_email(student)
                messages.success(request,
                                 "Account created successfully! Please check your email to verify your account first.")

            except Exception as e:
                print(f"Email error: {e}")
                messages.warning(request, "Account created, but we faced an issue sending the verification email.")

            return redirect('create_student')
    else:
        form = StudentForm()

    return render(request, "student/create_student.html", {
        "form": form
    })

def verify_student_account(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    action = request.GET.get('action')

    if student.account_status == True:
        messages.warning(request, "This verification link has already been used and is no longer valid.")
        return redirect('create_student')

    if action == "accept":
        student.account_status = True
        student.save()
        message = f"Success {student.first_name} your account is now ACTIVE."

        return render(request, "student/verification_result.html", {
            "message": message,
            "student": student,
            "success": True
        })

    elif action == "reject":
        student.account_status = False
        student.save()
        messages.error(request, f"Verification rejected for {student.first_name}. Please register again if needed.")
        return redirect('create_student')
    else:
        messages.error(request, "Invalid validation signature links.")
        return redirect('create_student')

def student_details(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    return render(
        request,
        "student/student_details.html",
        {"student": student}
    )

def student_update(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student_details', student_id=student.id)
    else:
        form = StudentForm(instance=student)

    return render(request, "student/student_details.html", {
        "form": form,
        "is_edit": True,
        "student": student
    })


def delete_student(request, student_id):
    if request.method == "POST":
        student = get_object_or_404(Student, id=student_id)
        student_name = f"{student.first_name} {student.last_name}"

        student.delete()

        messages.success(request, f"Student record for {student_name} has been successfully deleted.")

    return redirect('create_student')


def student_list(request):
    students = Student.objects.all().order_by('-id')
    return render(request, "student/student_list.html", {
        "students": students
    })
