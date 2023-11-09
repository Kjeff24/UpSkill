from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str 
from django.conf import settings
from django.core.mail import EmailMessage
from myapp.tokens import account_activation_token
from myapp.models import User
from myapp.forms import LoginForm, TutorSignUpForm, LearnerSignUpForm


def loginPage(request):
    """
    View function to handle user login.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template for the login page.
    """
    
    if request.user.is_authenticated:
        # User is already logged in
        return redirect('learner-home', request.user)  # Redirect to the dashboard page or any other desired page
    
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_learner and user.is_email_verified:
                    login(request, user)
                    return redirect('learner-home', pk=request.user)
                elif user.is_learner and not user.is_email_verified:
                    messages.add_message(request, messages.ERROR,
                                        'Your email is not verified.')
                else:
                    messages.add_message(request, messages.ERROR,
                                        'You are not authorized.')
            else:
                messages.add_message(request, messages.ERROR,
                                    'Invalid credentials, try again')
        else:
            messages.add_message(request, messages.ERROR,
                                'Error validating, try again')

    context = {'form': form}

    return render(request, "authenticate/login.html", context)


# Logout User
def logoutUser(request):
    """
    View function to handle user logout.

    Args:
        request: The HTTP request object.

    Returns:
        A redirection to the login page.
    """
    logout(request)
    return redirect('login')


# Leaner signup
def learnerSignupPage(request):
    """
    View function to handle learner signup.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template for the learner signup page.
    """
    if request.method == 'POST':
        form = LearnerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_email_verified = True
            user.save()
            # send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                         'You can login now')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = LearnerSignUpForm()

    context = {'form': form}

    return render(request, "authenticate/learner_signup.html", context)


# Employer Signup
def tutorSignupPage(request):
    """
    View function to handle tutor signup.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template for the employer signup page.
    """
    if request.method == 'POST':
        form = TutorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Assign staff status
            user.is_superuser = True  # Assign superuser status
            user.save()
            # send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                         'You can login now')
            return redirect('tutor_admin:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = TutorSignUpForm()

    context = {'form': form}

    return render(request, "authenticate/tutor_signup.html", context)

# sends activation code to the email
def send_activation_email(user, request):
    """
    Function to send activation email to the user.

    Args:
        user: The User object.
        request: The HTTP request object.

    Returns:
        None.
    """
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    
    # render a template file and pass in context
    email_body = render_to_string('authenticate/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })

    # create an email from using EmailMessage()
    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[user.email]
                         )

    # send email
    email.send()


# activate user
def activate_user(request, uidb64, token):
    """
    View function to activate user account.

    Args:
        request: The HTTP request object.
        uidb64 (str): The encoded user ID.
        token (str): The activation token.

    Returns:
        A rendered HTML template for successful account activation or activation failure.
    """

    # decode uid64 back to the user id, and get the user
    try:
        uid = force_str (urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    # checks the user and token with the token generated from token.py   
    if user and account_activation_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        if user.is_learner:
            return redirect(reverse('login'))
        return redirect(reverse('employer_admin:login'))

    return render(request, 'authenticate/activate-failed.html', {"user": user})
