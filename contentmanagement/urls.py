from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("questions", views.questions, name="questions"),
    path("health", views.health_check, name="health-check"),
]
