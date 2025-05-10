from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view
from .views import UserRegistrationView

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
]

# Look at these files
# config/api_router.py
# users/adapters.py

# Two scoops of django, book