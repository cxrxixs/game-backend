"""
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "grade_level",
            "latest_score",
            "high_score",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile"]
        read_only_fields = ["email"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        profile = instance.profile

        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return super().update(instance, validated_data)
"""

from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import Profile


class CustomRegisterSerializer(RegisterSerializer):
    grade_level = serializers.IntegerField(required=True, max_value=12, min_value=1)
    high_score = serializers.IntegerField(required=True, max_value=1600, min_value=0)

    def save(self, request):
        user = super().save(request)
        user.profile.grade_level = self.validated_data["grade_level"]
        user.profile.high_score = self.validated_data["high_score"]
        user.profile.latest_score = self.validated_data["latest_score"]
        user.profile.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "grade_level",
            "high_score",
            "latest_score",
        ]
