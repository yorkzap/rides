# rides/users/serializers.py

from rest_framework import serializers


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# class SignupSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password1 = serializers.CharField()
#     password2 = serializers.CharField()

#     def validate(self, data):
#         if data["password1"] != data["password2"]:
#             raise serializers.ValidationError("Passwords do not match.")
#         return data
