from rest_framework import permissions, status
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_api.serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_api.permissions import UserAuthenticatedSessionAPIView

class UserRegister(APIView):
    """
    API View for user registration.
    """
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
        data=request.data
        data["username"] = data["username"].lower()
        data["email"] = data.get("email", "").lower()

        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


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
        return Response(status=status.HTTP_200_OK)

        
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
        serializer = self.serializer_class(request.user, context={'request': request})
        user_data = serializer.data

        return Response({'user': user_data}, status=status.HTTP_200_OK)