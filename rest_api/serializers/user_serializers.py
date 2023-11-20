from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, status
from rest_framework.response import Response

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer is used to validate the data for a new user and create the user.
    """
    
    avatar = serializers.ImageField(write_only=True, required=False)
    
    class Meta:
        model = UserModel
        fields = ['username', 'email',
                  'first_name', "last_name", 'password', 'is_learner', 'is_tutor', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, clean_data):
        """
        Custom create method to handle user creation.

        Parameters:
        - validated_data (dict): Validated data received for user creation.

        Returns:
        - UserModel: The created user object.
        """
        avatar_data = clean_data.pop('avatar', None)

        user_obj = UserModel.objects.create_user(
            **clean_data
        )
        
        if avatar_data:
            user_obj.avatar = avatar_data
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

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer to change user password
    """
    model = UserModel
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'avatar']
        
    def update(self, instance, validated_data):
        """
        Maintain the avatar if not updated
        """
        # Handle the avatar separately to avoid setting it to null
        avatar_data = validated_data.pop('avatar', None)
        instance = super().update(instance, validated_data)

        if avatar_data:
            instance.avatar = avatar_data
            instance.save()

        return instance