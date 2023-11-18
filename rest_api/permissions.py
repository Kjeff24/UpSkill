from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class UserAuthenticatedSessionAPIView(APIView):
    """
    User APIView with IsAuthenticated permission, SessionAuthentication,
    and UserSerializer.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]