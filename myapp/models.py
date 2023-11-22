from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class User(AbstractUser):
    """
    Custom User model that includes both employees and employers.

    Fields:
        is_tutor (bool): Indicates whether the user is an employer.
        is_learner (bool): Indicates whether the user is an employee.
        is_email_verified (bool): Indicates whether the user's email is verified.
        my_employer (str): The employer associated with the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        bio (str): A text field for the user's bio.
        avatar (ImageField): An image field for the user's avatar.

    Methods:
        None
    """
    is_tutor = models.BooleanField("Is Tutor", default=False)
    is_learner = models.BooleanField("Is Learner", default=False)
    is_email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, default="avatar.svg")


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    # the below line concatenates your website's reset password URL and the reset email token which will be required at a later stage
    
    reset_password_url = "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    email_plaintext_message = f"Open the link to reset your password: {reset_password_url}"

    """
        this below line is the django default sending email function, 
        takes up some parameter (title(email title), message(email body), from(email sender), to(recipient(s))
    """
    send_mail(
        # title:
        "Password Reset for {title}".format(title="UpSkill portal account"),
        # message:
        email_plaintext_message,
        # from:
        "upskill@training.com",
        # to:
        [reset_password_token.user.email],
        fail_silently=False,
    )
