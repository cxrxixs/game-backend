from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"gamematch", views.GameMatchViewSet, basename="gamematch")
router.register(r"gamematchplayer", views.GameMatchPlayerViewSet, basename="gamematchplayer")


urlpatterns = [
    path("home/", views.index, name="home"),
    path("", include(router.urls)),
]
