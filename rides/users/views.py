# rides/users/views.py

from allauth.account.forms import LoginForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import SignupForm
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rides.users.models import User

from .serializers import LoginSerializer
from .serializers import PasswordResetSerializer
from .serializers import SignupSerializer


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class PasswordResetView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        form = ResetPasswordForm(data={"email": serializer.validated_data["email"]})
        if form.is_valid():
            form.save(request._request)
            return Response(
                {"detail": _("Password reset email has been sent.")},
                status=status.HTTP_200_OK,
            )

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        role = serializer.validated_data["role"]

        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": "User with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
        )

        send_email_confirmation(request, user)

        return Response(
            {
                "detail": "User created successfully.",
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )

        django_login(request, user)

        if user.role == User.Role.ADMIN:
            redirect_url = "admin_url"
        elif user.role == User.Role.DRIVER:
            redirect_url = "driver_url"
        elif user.role == User.Role.RIDER:
            redirect_url = "rider_url"
        else:
            redirect_url = reverse("users:detail", kwargs={"pk": user.pk})

        return Response(
            {
                "detail": "Logged in successfully.",
                "email": user.email,
                "role": user.role,
                "redirect_url": redirect_url,
            },
            status=status.HTTP_200_OK,
        )
