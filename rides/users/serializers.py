from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["id", "email", "name", "role", "password"]
        extra_kwargs = {
            "role": {"required": True},
        }

    def validate_role(self, value):
        """Ensure the role is either Rider or Attendant."""
        valid_roles = [User.Role.RIDER, User.Role.ATTENDANT]
        if value not in valid_roles:
            raise serializers.ValidationError("Invalid role. Choose either 'Rider' or 'Attendant'.")
        return value

    def create(self, validated_data):
        """Create a new user with the provided role and hashed password."""
        user = User.objects.create_user(**validated_data)
        return user
