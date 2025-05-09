from django.urls import path

from .views import LoginView
from .views import PasswordResetView
from .views import SignupView
from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("~password-reset", PasswordResetView.as_view(), name="api_password_reset"),
    path("~login_api", LoginView.as_view(), name="login_api"),
    path("~signup_api", SignupView.as_view(), name="signup_api"),
]
