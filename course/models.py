from django.db import models
from myapp.models import User
from event.models import Event
from datetime import timedelta
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
import pytz

# Create your models here.
# Course model allows employers to create course
class Course(models.Model):
    """
    Model representing a course created by an employer.

    A course has a name, description, instructor (ForeignKey to User), creation date, and last update date.

    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE,db_constraint=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


# Resources model allows employers to add resources based on course
class Resource(models.Model):
    """
    Model representing a resource associated with a course.

    A resource has a name, course (ForeignKey to Course), description, file type, YouTube link, file upload, creation
    date, last update date, user download count, and user email sent count.

    """
    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('link', 'link'),
    )
    
    name = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField(max_length=50, blank=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default="null")
    youtubeLink = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/', blank=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_download_count = models.PositiveIntegerField(default=0)
    user_email_sent = models.PositiveIntegerField(default=0)

    def download_count(self):
        """
        Increment the user download count by 1 and save the resource.

        """
        self.user_download_count += 1
        self.save()

    def email_count(self):
        """
        Increment the user email sent count by 1 and save the resource.

        """
        self.user_email_sent += 1
        self.save()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Override the save method to create an event for the resource.

        After saving the resource, an event is created with the resource's name, associated course, start time, and end time.

        """
        # Call the parent class's save() method
        super().save(*args, **kwargs)
        
        timezone_str = 'GMT0'  # Replace 'Your_Timezone' with your desired timezone
        timezone_obj = pytz.timezone(timezone_str)

        # Get the current time in the desired timezone
        current_time = timezone.localtime(timezone.now(), timezone_obj)

        # Create an event for the announcement
        event = Event.objects.create(
            name=self.name,
            course=self.course,
            start=current_time,
            end=current_time + timezone.timedelta(hours=24)  # Adjust the end time as needed
        )
        event.save()
        
@receiver(post_delete, sender=Resource)
def delete_associated_event(sender, instance, **kwargs):
    """
    Signal receiver to delete the associated event when a resource is deleted.

    This signal receiver is triggered after deleting a resource. It looks for an event with the same name as the deleted
    resource and deletes it if found.

    """
    event = Event.objects.filter(name=instance.name).first()
    if event:
        event.delete()
        

# Announcement model allows employers to add announcements based on course
class Announcement(models.Model):
    """
    Model representing an announcement associated with a course.

    An announcement has a title, content, course (ForeignKey to Course), creation date, and last update date.

    """
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Override the save method to create an event for the announcement.

        After saving the announcement, an event is created with the announcement's title, associated course, start time,
        and end time.

        """
        # Call the parent class's save() method
        super().save(*args, **kwargs)

        # Create an event for the announcement
        event = Event.objects.create(
            name=self.title,
            course=self.course,
            start=self.date,
            end=self.date + timedelta(hours=36)  # Adjust the end time as needed
        )
        event.save()
        
@receiver(post_delete, sender=Announcement)
def delete_associated_event(sender, instance, **kwargs):
    """
    Signal receiver to delete the associated event when an announcement is deleted.

    This signal receiver is triggered after deleting an announcement. It looks for an event with the same name as the
    deleted announcement and deletes it if found.

    """
    event = Event.objects.filter(name=instance.title).first()
    if event:
        event.delete()
    
# Room allows employees to chat
class Room(models.Model):
    """
    Model representing a chat room associated with a course.

    A room has a room topic, course (ForeignKey to Course), room description, creation date, and last update date.

    """
    room_topic = models.CharField(max_length=200, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    room_description = models.TextField(null=True, blank=True)
    created  = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_topic
    
# Message allows host and participants to converse
class Message(models.Model):
    """
    Model representing a message in a chat room.

    A message has a user (ForeignKey to User), room (ForeignKey to Room), message body, creation date, and last update
    date.

    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
    
    
# Course Participants
class Participants(models.Model):
    """
    Model representing a participant in a course.

    A participant has a user (ForeignKey to User), course (ForeignKey to Course), room (ForeignKey to Room), user
    download count, and user email sent count.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE) 
    room =  models.ForeignKey(Room, on_delete=models.SET_NULL, null=True) 
    user_download_count = models.PositiveIntegerField(default=0)
    user_email_sent = models.PositiveIntegerField(default=0)

    def download_count(self):
        """
        Increment the user download count by 1 and save the participant.

        """
        self.user_download_count += 1
        self.save()

    def email_count(self):
        """
        Increment the user email sent count by 1 and save the participant.

        """
        self.user_email_sent += 1
        self.save()
        
    def has_course(self):
        """
        Check if the participant has an associated course.

        Returns:
            bool: True if the participant has a course, False otherwise.

        """
        return self.course is not None
        
    def __str__(self):
        return str(self.user)
    
class VideoStreamMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name