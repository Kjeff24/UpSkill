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


# Employee signup
class EmployeeSignUpForm(UserCreationForm):
    """
    Form for employee sign up.

    Inherits from UserCreationForm and adds additional fields such as first name,
    last name, email, and employer selection.
    """
    # Create a modelchoicefield to display only employers
    employer_select = forms.ModelChoiceField(
        queryset=User.objects.filter(is_employer=True), widget=forms.Select(attrs={'class': 'form-select'}))
    
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
    is_employee = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'is_employee', 'employer_select')

    # Based on the employer the user select, it it assigned to my_employer field in User model
    def save(self, commit=True):
        """
        Saves the form data and associates the selected employer with the user instance.

        Args:
            commit (bool, optional): Determines whether to save the user instance immediately to the database. 
                                    Defaults to True.

        Returns:
            User: The saved user instance.

        Raises:
            None
        """
        user = super().save(commit=False)
        user.my_employer = self.cleaned_data['employer_select']
        if commit:
            user.save()
        return user


# Employer Signup
class EmployerSignUpForm(UserCreationForm):
    """
    Form for employer sign up.

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
    is_employer = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2', 'is_employer')


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
