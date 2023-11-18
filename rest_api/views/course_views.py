from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from course.models import Course, Resource, Announcement, Room, Message, Participants
from rest_api.serializers import *
from rest_api.permissions import UserAuthenticatedSessionAPIView



class CourseListView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for listing courses based on the current user's participation.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ResourceListView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    serializer_class = ResourceSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter resources based on the courses where the user is a participant
        queryset = Resource.objects.filter(course__in=participant_courses)

        return queryset

class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class AnnouncementListView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter announcement based on the courses where the user is a participant
        queryset = Announcement.objects.filter(course__in=participant_courses)

        return queryset

class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnouncementSerializer

class RoomListView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter room based on the courses where the user is a participant
        queryset = Room.objects.filter(course__in=participant_courses)

        return queryset

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class MessageListView(UserAuthenticatedSessionAPIView, generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter messages based on the rooms associated with the participant's courses
        queryset = Message.objects.filter(room__course__in=participant_courses)

        return queryset

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ParticipantsListView(UserAuthenticatedSessionAPIView, generics.ListCreateAPIView):
    serializer_class = ParticipantsSerializer
    
    def get_queryset(self):
        learner = self.request.user
        return Participants.objects.filter(user=learner)
    
    def create(self, request, *args, **kwargs):
        # Check if a participant with the same user and course already exists
        user=request.user
        course=request.data.get('course')
        get_course = Course.objects.get(pk=course)
        existing_participant = Participants.objects.filter(
            user=user,
            course=course
        ).first()

        if existing_participant:
            # If participant already exists, return a custom response
            return Response(
                {'error': f"You have already enrolled in {get_course}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If participant does not exist, proceed with the creation
        return super().create(request, *args, **kwargs)

class ParticipantsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer
