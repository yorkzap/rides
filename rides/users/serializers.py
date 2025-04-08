# rides/users/serializers.py

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
