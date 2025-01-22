from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"match", views.GameMatchViewSet, basename="match")
# router.register(r"players", views.GameMatchPlayerViewSet, basename="players")
router.register("round", views.GameRoundViewSet, basename="round")
router.register("answer", views.PlayerAnswerViewSet, basename="answer")

urlpatterns = [
    path("summary/", views.summary, name="match-summary"),
    path("", include(router.urls)),
]
