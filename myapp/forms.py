from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User

# login form


class LoginForm(forms.Form):
    """
    Form for user login.

    Provides fields for username and password entry.
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username",
                "autocomplete": "username",
                "placeholder": "Enter your username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "passwordField",
                "autocomplete": "password",
                "placeholder": "Enter your password",
            }
        )
    )


# Learner signup
class LearnerSignUpForm(UserCreationForm):
    """
    Form for learner sign up.

    Inherits from UserCreationForm and adds additional fields such as first name,
    last name, email, and tutor selection.
    """
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "first_name",
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "last_name",
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "username",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "passwordField1"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "passwordField2"
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "autocomplete": "email",
            }
        )
    )
    is_learner = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'is_learner')



# tutor Signup
class TutorSignUpForm(UserCreationForm):
    """
    Form for tutor sign up.

    Inherits from UserCreationForm and adds additional fields such as first name,
    last name, and email.
    """
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "first_name",
                'id': 'floatingfirst_name',
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "last_name",
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "username",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "passwordField1"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "passwordField2"
            }
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "autocomplete": "email",
            }
        )
    )
    is_tutor = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2', 'is_tutor')


# User Form
class UserForm(ModelForm):
    """
    Form for updating user information.

    Provides fields for updating the user's first name, last name, username, bio, and avatar.
    """
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        ),
        required=False
    )

    avatar = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Retrieve the 'user' argument from kwargs
        super().__init__(*args, **kwargs)
