from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer is used to validate the data for a new user and create the user.
    """
    class Meta:
        model = UserModel
        fields = ['username', 'email',
                  'first_name', "last_name", 'password', 'is_learner', 'is_tutor']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, clean_data):
        """
        Custom create method to handle user creation.

        Parameters:
        - validated_data (dict): Validated data received for user creation.

        Returns:
        - UserModel: The created user object.
        """

        user_obj = UserModel.objects.create_user(
            **clean_data
        )
        user_obj.save()
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    This serializer is used to validate the data for a user login. It includes fields for 'username' and 'password'.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        """
        Method to authenticate the user based on provided credentials.

        Parameters:
        - clean_data (dict): Dictionary containing 'username' and 'password' for authentication.

        Returns:
        - user: Authenticated user object if successful, otherwise raises a ValidationError.
        """
        user = authenticate(
            username=clean_data['username'], password=clean_data['password'])
        if not user:
            raise serializers.ValidationError(
                'user not found, check your credentials')
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserModel
    """
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email',
                  'is_learner', 'first_name', 'last_name', 'bio', 'avatar']
        read_only_fields = ['avatar']

    def get_avatar(self, user):
        """
        Get the absolute URL of the user's avatar.

        Parameters:
        - user: User object.

        Returns:
        - str: Absolute URL of the user's avatar or None if the avatar is not available.
        """
        if user.avatar:
            # Assuming MEDIA_URL is configured in your Django settings
            return self.context['request'].build_absolute_uri(user.avatar.url)
        return None
