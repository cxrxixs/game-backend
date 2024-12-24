from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import Context, Template

from .models import Question


def index(request: HttpResponse):
    return render(request, "index.html", context={"title": "Home"})


def questions(request: HttpResponse):
    queryset = Question.objects.select_related("solution").all()

    return render(request, "questions.html", context={"title": "Questions", "questions": queryset})
