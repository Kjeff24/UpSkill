from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.models import User
from course.models import Course, Participants
from django.core.exceptions import ObjectDoesNotExist



# Employee home
@login_required(login_url='login')
def employeeHome(request, pk):
    """
    View function for the employee home page.

    Args:
        request: The HTTP request object.
        pk: The primary key of the user.

    Returns:
        A rendered HTML template for the employee home page, which includes the enrollment form
        and a list of available courses. If a course is selected for enrollment, the user is
        enrolled in the course and appropriate success messages are displayed.
    """
    employee = request.user
    try:
        employer = User.objects.get(username=employee.my_employer)

        employer_courses = Course.objects.filter(instructor__username=employer).distinct()
        
        participants = Participants.objects.filter(user=employee)
        courses = [participant.course for participant in participants]

        context = {'courses': courses, 'employer_courses': employer_courses}

        if request.method == 'POST':
            course_selected = request.POST.get('course')

            course, created = Course.objects.get_or_create(name=course_selected)
            user = User.objects.get(username=request.user.username)

            enrollment= Participants.objects.filter(course=course)

            if enrollment.filter(user=user).exists():
                messages.success(request, 'You have already enrolled.')
                return redirect('employee-home', pk=request.user)
            else:
                participant = Participants.objects.create(user=user, course=course)
                messages.success(request, 'Enrollment successful.')
                return redirect('enrollment-success')
        
        return render(request, "usersPage/employee_home.html", context)
    
    except ObjectDoesNotExist:
        return HttpResponse("You are not authorized")


def enrollmentSuccess(request):
    """
    View function for the enrollment success page.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template for the enrollment success page.
    """
    if request.method == 'POST':
        messages.success(request, 'You have already enrolled.')
        return redirect('employee-home', pk=request.user)
    
    return render(request, "usersPage/enrollment_success.html")