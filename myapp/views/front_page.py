from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    """
    View function to render the home page.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template for the home page.
    """
    return render(request, "frontPage/home.html")
