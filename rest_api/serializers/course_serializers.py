from rest_framework import serializers
from course.models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'instructor', 'name', 'description']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'course', 'description', 'file_type', 'youtubeLink', 'file', 'created', 'updated']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'course', 'created', 'updated']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        # Dynamically set the queryset for the user field to only include the request.user
        request = kwargs['context']['request']
        user_queryset = User.objects.filter(pk=request.user.pk)
        self.fields['user'].queryset = user_queryset
        
        # Dynamically set the queryset for the room field to only include rooms the user belongs to
        room_queryset = Room.objects.filter(course__participants__user=request.user)
        self.fields['room'].queryset = room_queryset
        super().__init__(*args, **kwargs)

class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['user', 'course']
        
    def __init__(self, *args, **kwargs):
        # Dynamically set the queryset for the user field to only include the request.user
        request = kwargs['context']['request']
        user_queryset = User.objects.filter(pk=request.user.pk)
        self.fields['user'].queryset = user_queryset
        super().__init__(*args, **kwargs)
