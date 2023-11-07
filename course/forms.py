from .models import Course, Resource, Announcement, Room
from django.forms import ModelForm
from django import forms
from myapp.models import User

# Course form
class CourseForm(ModelForm):
    """
    Form class for creating or updating a Course.

    This form is used for creating or updating a Course object. It inherits from Django's ModelForm class and defines
    the Course model as the model to be used for the form. It includes all fields of the Course model except
    'course_participants' and 'instructor'.

    """
    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['course_participants', 'instructor']


# Resource form
class ResourceForm(ModelForm):
    """
    Form class for creating or updating a Resource.

    This form is used for creating or updating a Resource object. It inherits from Django's ModelForm class and defines
    the Resource model as the model to be used for the form. It includes fields such as 'name', 'course', 'description',
    'youtubeLink', and 'file'. The 'course' field is customized to show only courses created by the employer (user).

    """
    # Shows only courses, created by the employer
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Retrieve the 'user' argument from kwargs
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(instructor=user)

    class Meta:
        model = Resource
        fields = ['name', 'course', 'description', 'youtubeLink', 'file']


# Annoucement form class AnnouncementForm(forms.ModelForm):
class AnnouncementForm(ModelForm):
    """
    Form class for creating or updating an Announcement.

    This form is used for creating or updating an Announcement object. It inherits from Django's ModelForm class and
    defines the Announcement model as the model to be used for the form. It includes fields such as 'title', 'content',
    and 'course'. The 'course' field is customized to show only courses created by the employer (user).

    """
    # Shows only courses, created by the employer
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Retrieve the 'user' argument from kwargs
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(instructor=user)

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'course']


# Room form
class RoomForm(ModelForm):
    """
    Form class for creating or updating a Room.

    This form is used for creating or updating a Room object. It inherits from Django's ModelForm class and defines
    the Room model as the model to be used for the form. It includes fields such as 'room_topic', 'course',
    and 'room_description'. The 'course' field is customized to show only courses created by the employer (user).

    """
    # Shows only courses, created by the employer
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Retrieve the 'user' argument from kwargs
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(instructor=user)
        
    class Meta:
        model = Room
        fields = ['room_topic', 'course', 'room_description']
