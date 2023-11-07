from django.contrib import admin
from .models import *

class ParticipantsInline(admin.TabularInline):
    """
    Inline admin class for Participants.

    This inline admin class defines the tabular layout for the Participants model in the Django admin interface. It allows
    managing the participants of a course directly from the course's admin page.

    """
    model = Participants

class CourseAdmin(admin.ModelAdmin):
    """
    Admin class for Course model.

    This admin class customizes the Course model's representation in the Django admin interface. It defines the behavior
    and appearance of the Course model's admin page.

    """
    inlines = [ParticipantsInline]

# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(Resource)
admin.site.register(Announcement)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Participants)
admin.site.register(VideoStreamMember)