from django.db import models

# Create your models here.
class Event(models.Model):
    """
    Model representing an event.

    Fields:
        id (AutoField): Primary key for the event.
        name (CharField): Name of the event (max length: 255 characters).
        course (ForeignKey): Foreign key to the 'Course' model, representing the course associated with the event.
        start (DateTimeField): Start date and time of the event.
        end (DateTimeField): End date and time of the event.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return f"{self.id} - {self.name}"