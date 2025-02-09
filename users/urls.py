"""
from django.urls import path

from .views import GoogleLogin, user_profile

urlpatterns = [
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("profile/", user_profile, name="user_profile"),
]
"""

from django.urls import path

from .views import GoogleLoginView, ProfileDetailView

urlpatterns = [
    path("auth/google/", GoogleLoginView.as_view(), name="google_login"),
    path("profile/", ProfileDetailView.as_view(), name="profile_detail"),
]
