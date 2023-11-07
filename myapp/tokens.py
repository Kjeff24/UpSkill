from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  

# Generate token by inheriting PasswordResetTokenGenerator
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation.

    Methods:
        _make_hash_value(self, user, timestamp): Override method to generate a unique hash value based on user and timestamp.
    """
    def _make_hash_value(self, user, timestamp):
        """
        Generate a unique hash value based on the user and timestamp.

        Args:
            user: The user object for which the token is generated.
            timestamp: The timestamp when the token is generated.

        Returns:
            str: The hash value.

        """
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))
        
# Create an instance of the custom token generator
account_activation_token = AccountActivationTokenGenerator()