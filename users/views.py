from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import ProfileSerializer


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client  # Required by dj-rest-auth

    def post(self, request, *args, **kwargs):
        # Perform the social login
        response = super().post(request, *args, **kwargs)

        # Check if login was successful
        if response.status_code == status.HTTP_200_OK:
            user = self.user
            profile = user.profile
            data = {
                "key": response.data.get("key"),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "grade_level": profile.grade_level,
                    "high_score": profile.high_score,
                    "latest_score": profile.latest_score,
                },
            }
            return Response(data, status=status.HTTP_200_OK)

        # Otherwise, return the original response (likely errors)
        return response


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
