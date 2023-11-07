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

def about(request):
    """
    View function to render the about page.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template for the about page.
    """
    return render(request, "frontPage/about.html")

def contact(request):
    """
    View function to handle the contact form submission.

    Args:
        request: The HTTP request object.

    Returns:
        A redirection to the contact page after submitting the form,
        or a rendered HTML template for the contact page if it's a GET request.
    """
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        country = request.POST.get('country')
        from_message = request.POST.get('message')
        
        send_mail(
            subject="Message from Contact Form",
            message=f'Name: {first_name} {last_name}\nEmail: {email}\nCountry: {country}\n\nMessage: {from_message}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        messages.add_message(request, messages.SUCCESS,
                                         'Your email has been successfully sent')  
        return redirect('contact') 
            
    context = {
        'page': 'contact'
    }
    return render(request, "frontPage/contact.html", context)
