from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.response import Response

from rest_api.serializers import QuizSerializer, ResultSerializer
from rest_api.permissions import UserAuthenticatedSessionAPIView


from django.db.models import F, Q, Count

from quiz.models import Quiz, Question, Answer, Result
from course.models import Course, Participants

class QuizListView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for listing quizzes based on the current user's participation of a course.
    """
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter quizzes based on the courses where the user is a participant
        return Quiz.objects.filter(course__in=participant_courses)

class QuizDetailView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for a quiz based on the current user's participation of a course.
    """
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        user = self.request.user
        course_id = self.kwargs.get('pk')
        
        # Assuming you have a Participant model to represent the user's participation in a course
        participant = Participants.objects.filter(user=user, course_id=course_id).first()

        if not participant:
            # Handle the case where the user is not a participant in the specified course
            return Quiz.objects.none()
        
        # Filter quizzes that the user has not attempted more than quiz_chances times
        quizzes = Quiz.objects.filter(
            course_id=course_id
        ).annotate(
            result_count=Count('result', filter=Q(result__user=user))
        ).filter(
            result_count__lt=F('quiz_chances')
        )
        print(quizzes)
        # Filter quizzes that have questions
        filtered_quizzes = [
            quiz for quiz in quizzes if quiz.question_set.exists()
        ]
        return filtered_quizzes
    
    
class QuizDataAPIView(UserAuthenticatedSessionAPIView, views.APIView):
    """
    API View to get quiz and it's related answers data.
    """
    def get(self, request, pk, format=None):
        quiz = get_object_or_404(Quiz, pk=pk)
        questions = []
        for q in quiz.get_questions():
            answers = []
            for a in q.get_answers():
                answers.append(a.text)
            questions.append({str(q): answers})
        return Response({
            'data': questions,
            'time': quiz.time,
        })
        
        
class QuizSubmissionAPIView(UserAuthenticatedSessionAPIView, views.APIView):
    """
    API View to save quiz taken by user.
    """
    def post(self, request, pk, format=None):
        """
        Handle POST request to save quiz submission.

        Parameters:
        - request: The HTTP request object.
        - pk: The primary key of the quiz being submitted.
        - format: The desired response format.

        Returns:
        - Response: JSON response indicating whether the user passed the quiz, the score, and detailed results.
        """
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        # save completion time from response data
        completionTime = float(data_["completionTime"][0])

        # remove csrfmiddlewaretoken and completionTime, and returns the list of questions
        data_.pop('csrfmiddlewaretoken')
        data_.pop('completionTime')

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions

        results = self.process_quiz_results(questions, request)

        score_ = score * multiplier
        save_result = Result.objects.create(quiz=quiz, user=user, score=score_, completion_time=completionTime)
        save_result.save()

        if score_ >= quiz.required_score_to_pass:
            return Response({'passed': True, 'score': score_, 'results': results})
        else:
            return Response({'passed': False, 'score': score_, 'results': results})

    def process_quiz_results(self, questions, request):
        """
        Process the quiz results based on the selected answers.

        Args:
            questions (list): List of Question objects.
            request: The request object containing the selected answers.

        Returns:
            list: A list of dictionaries containing information about each question's correctness.
        """
        results = []

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                correct_answer = self.check_answer(q, a_selected)
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        return results

    def check_answer(self, question, selected_answer):
        """
        Check if the selected answer for a given question is correct.

        Parameters:
        - question: The Question object for which the answer is checked.
        - selected_answer: The selected answer for the question.

        Returns:
        - The correct answer text if the selected answer is correct; otherwise, None.
        """
        question_answers = Answer.objects.filter(question=question)

        for a in question_answers:
            if selected_answer == a.text:
                return a.text if a.correct else None

        return None
        

class ResultListAPIView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for listing results based on the current user's quiz taken
    """
    serializer_class = ResultSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter quizzes based on the courses where the user is a participant
        quizzes =  Quiz.objects.filter(course__in=participant_courses)
        
        return Result.objects.filter(quiz__in = quizzes)