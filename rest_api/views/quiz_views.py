from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_api.serializers import QuizSerializer
from rest_api.permissions import UserAuthenticatedSessionAPIView


from django.db.models import F, Q, Count

from quiz.models import Quiz
from course.models import Course

class QuizListView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for listing quizzes based on the current user's participation of a course.
    """
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter quizzes based on the courses where the user is a participant
        queryset = Quiz.objects.filter(course__in=participant_courses)

        return queryset

class QuizDetailView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for a quiz based on the current user's participation of a course.
    """
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        user = self.request.user
        course_id = self.kwargs.get('pk')
        
        course = Course.objects.get(id=course_id)
        
        # Filter quizzes that the user has not attempted more than quiz_chances times
        quizzes = Quiz.objects.filter(
            course=course
        ).annotate(
            result_count=Count('result', filter=Q(result__user=user))
        ).filter(
            result_count__lt=F('quiz_chances')
        )

        # Filter quizzes that have questions
        filtered_quizzes = [
            quiz for quiz in quizzes if quiz.question_set.exists()
        ]

        return filtered_quizzes