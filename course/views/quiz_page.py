from django.shortcuts import render
from course.models import Course
from quiz.models import Result

# room page
def quizPage(request, pk):
    """
    Render the quiz page for a course.

    This view function retrieves the necessary data to display the quiz page for a specific course. It fetches the
    courses in which the employee is a participant and retrieves the specific course based on the provided primary key (pk).

    Parameters:
    - request: The HTTP request object generated by the user's interaction with the web application.
    - pk: The primary key of the course for which the quiz page is being accessed.

    Returns:
    - The function renders the quiz page template with the necessary context data.

    """
    employee = request.user

    courses = Course.objects.filter(participants__user=employee)
    course = Course.objects.get(id=pk)
    
    # Filter results based on the user and course
    user_results = Result.objects.filter(user=employee, quiz__course=course).order_by('-created')
    
    context = {
        "course":course, 
        'courses':courses,
        'user_results':user_results
    }

    return render(request, "page/quiz_page.html", context)