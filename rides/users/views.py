from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from rides.users.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.account.forms import ResetPasswordForm
from .serializers import PasswordResetSerializer
from rest_framework.permissions import AllowAny

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
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
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
        form = ResetPasswordForm(data={'email': serializer.validated_data['email']})

        if form.is_valid():

            form.save(request)
            return Response({'detail': _('Password reset email has been sent.')}, status=status.HTTP_200_OK)
        
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

