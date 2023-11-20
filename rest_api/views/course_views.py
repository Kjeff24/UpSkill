from rest_framework.exceptions import NotFound

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from course.models import Course, Resource, Announcement, Room, Message, Participants
from rest_api.serializers import *
from rest_api.permissions import UserAuthenticatedSessionAPIView



class CourseListAPIView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for listing courses based on the current user's participation of a course.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
class CourseDetailAPIView(UserAuthenticatedSessionAPIView, generics.RetrieveAPIView):
    """
    Retrieve the queryset for a course based on the current user's participation of a course.
    """
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # if not participant_courses:
        #     return []
        
        return participant_courses
            

class ResourceListAPIView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for listing resources based on the current user's participation of a course.
    """
    serializer_class = ResourceSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter resources based on the courses where the user is a participant
        queryset = Resource.objects.filter(course__in=participant_courses)

        return queryset
    
class ResourceDetailAPIView(UserAuthenticatedSessionAPIView, generics.RetrieveAPIView):
    """
    Retrieve the queryset for a resource based on the current user's participation of a course.
    """
    serializer_class = ResourceSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter resources based on the courses where the user is a participant
        queryset = Resource.objects.filter(course__in=participant_courses)

        return queryset


class AnnouncementListAPIView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for listing announcements based on the current user's participation of a course.
    """
    serializer_class = AnnouncementSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter announcement based on the courses where the user is a participant
        queryset = Announcement.objects.filter(course__in=participant_courses)

        return queryset
    
class AnnouncementDetailAPIView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for an announcement based on the current user's participation of a course.
    """
    serializer_class = AnnouncementSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter announcement based on the courses where the user is a participant
        queryset = Announcement.objects.filter(course__in=participant_courses)

        return queryset


class RoomListAPIView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for listing rooms based on the current user's participation of a course.
    """
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter room based on the courses where the user is a participant
        queryset = Room.objects.filter(course__in=participant_courses)

        return queryset
    
class RoomDetailAPIView(UserAuthenticatedSessionAPIView, generics.ListAPIView):
    """
    Retrieve the queryset for a room based on the current user's participation of a course.
    """
    serializer_class = RoomSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter room based on the courses where the user is a participant
        queryset = Room.objects.filter(course__in=participant_courses)

        return queryset

class MessageListAPIView(UserAuthenticatedSessionAPIView, generics.ListCreateAPIView):
    """
    Retrieve the queryset for listing messages based on the current user's participation of a course.
    """
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter messages based on the rooms associated with the participant's courses
        queryset = Message.objects.filter(room__course__in=participant_courses)

        return queryset

class MessageDetailAPIView(UserAuthenticatedSessionAPIView, generics.ListCreateAPIView):
    """
    Retrieve the queryset for a message based on the current user's participation of a course.
    """
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        # Get the courses where the request.user is a participant
        participant_courses = Course.objects.filter(participants__user=self.request.user)

        # Filter messages based on the rooms associated with the participant's courses
        queryset = Message.objects.filter(room__course__in=participant_courses)

        return queryset


class ParticipantsListAPIView(UserAuthenticatedSessionAPIView, generics.ListCreateAPIView):
    """
    Retrieve the queryset for listing participcipants.
    """
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

