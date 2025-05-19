# rides/users/serializers.py

from rest_framework import serializers

from rides.users.models import User


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
