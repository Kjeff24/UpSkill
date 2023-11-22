from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, views, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_api.serializers import (UserRegisterSerializer, UserLoginSerializer,
                                  UserSerializer, ChangePasswordSerializer, UserUpdateSerializer)
from rest_api.permissions import UserAuthenticatedSessionAPIView

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.core.mail import EmailMessage
from myapp.tokens import account_activation_token
from django.shortcuts import render, redirect, reverse

UserModel = get_user_model()


class UserRegister(generics.GenericAPIView):
    """
    API View for user registration.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        API endpoint for user registration.

        This view handles user registration by receiving user data in the request.
        It converts the username and email to lowercase, creates a new user using
        the provided data, and returns a response with the user details if successful.

        Parameters:
        - request: The HTTP request object containing user registration data.

        Returns:
        - If the registration is successful, returns a response with user details
            and a status of HTTP 201 Created. If there is an error in the registration
            process, returns a response with HTTP 400 Bad Request.
        """
        data = request.data

        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                # Send confirmation email
                self.send_activation_email(user, request)
                return Response({"message": "Verification email has been sent to your account"}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def send_activation_email(self, user, request):
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
        email_body = render_to_string('authenticate/api_activate_user.html', {
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


class UserLogin(APIView):
    """
    API View for user login.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        """
        API endpoint for user login.

        This view handles user login by receiving user login data in the request.
        It converts the username to lowercase, validates the data using the
        UserLoginSerializer, and checks user credentials. If the login is successful,
        the user is logged in, and a response with user details is returned.

        Parameters:
        - request: The HTTP request object containing user login data.

        Returns:
        - If the login is successful, returns a response with user details and a
          status of HTTP 200 OK. If there is an error in the login process, returns
          a response with HTTP 400 Bad Request.
        """
        data = request.data
        data["username"] = data["username"].lower()
        user = get_object_or_404(UserModel, username=data['username'])
         # If the password is correct, generate or get the user's token
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response({"user":serializer.data, "token": token.key}, status=status.HTTP_200_OK)


class UserLogout(APIView):
    """
    API View for user logout.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        """
        API endpoint for user logout.

        This view handles user logout by logging out the current user.

        Parameters:
        - request: The HTTP request object for user logout.

        Returns:
        - Returns a response with HTTP 200 OK, indicating a successful logout.
        """
        logout(request)
        return Response({"message":"Logout successful"}, status=status.HTTP_200_OK)


class UserView(UserAuthenticatedSessionAPIView, APIView):
    """
    API View to get logged in user details.
    """
    serializer_class = UserSerializer

    def get(self, request):
        """
        API endpoint to retrieve user details.

        This view retrieves user details for the authenticated user.

        Parameters:
        - request: The HTTP request object for retrieving user details.

        Returns:
        - Returns a response with user details and HTTP 200 OK status.
        """
        serializer = self.serializer_class(
            request.user, context={'request': request})
        user_data = serializer.data

        return Response({'user': user_data}, status=status.HTTP_200_OK)


class UserUpdateAPIView(UserAuthenticatedSessionAPIView, generics.RetrieveUpdateAPIView):
    """
    API View for updating user details.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self):
        # Retrieve the user instance based on the request's user
        return self.request.user 
    
class UserChangePasswordAPIView(UserAuthenticatedSessionAPIView, views.APIView):
    """
    API View to change user password.
    """
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')
            confirm_new_password = serializer.data.get('confirm_new_password')

            if not request.user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            if new_password != confirm_new_password:
                return Response({"new_password": ["New password and confirm new password do not match."]}, status=status.HTTP_400_BAD_REQUEST)

            request.user.password = make_password(new_password)
            request.user.save()
            return Response({"message":"Password changed successfully"}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserActivateAPIView(APIView):
    """
    API View to activate user account.
    """

    def get(self, request, uidb64, token):
        """
        Endpoint to activate user account.

        Args:
            request: The HTTP request object.
            uidb64 (str): The encoded user ID.
            token (str): The activation token.

        Returns:
            A JSON response for successful account activation or activation failure.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except Exception as e:
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_email_verified = True
            user.save()

            return redirect(reverse('user'))

        return render(request, 'authenticate/activate-failed.html', {"user": user})  # Rendering a failure HTML template
