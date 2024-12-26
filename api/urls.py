from django.urls import path

from . import views

urlpatterns = [
    path("questions/", views.question_list, name="api-questions"),
]
