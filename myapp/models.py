from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

# User models that includes employee and employers
class User(AbstractUser):
    """
    Custom User model that includes both employees and employers.

    Fields:
        is_employer (bool): Indicates whether the user is an employer.
        is_employee (bool): Indicates whether the user is an employee.
        is_email_verified (bool): Indicates whether the user's email is verified.
        my_employer (str): The employer associated with the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        bio (str): A text field for the user's bio.
        avatar (ImageField): An image field for the user's avatar.

    Methods:
        None
    """
    is_tutor = models.BooleanField("Is employer",default=False)
    is_learner = models.BooleanField("Is employee", default=False)
    is_email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
