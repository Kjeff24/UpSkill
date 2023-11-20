from rest_framework import serializers
from quiz.models import Quiz, Question, Answer, Result
from myapp.models import User
from rest_api.serializers import UserSerializer


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for get Quiz model
    """
    class Meta:
        model = Quiz
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    """
    Serializer for get Result model
    """
    user = UserSerializer()

    class Meta:
        model = Result
        fields = ['id', "user", "quiz", "score", "completion_time", "created"]
