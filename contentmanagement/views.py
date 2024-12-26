from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render

from .models import Question


def index(request: HttpResponse):
    return render(request, "index.html", context={"title": "Home"})


def questions(request: HttpResponse):
    try:
        queryset = Question.objects.select_related("solution").all()
        return render(request, "questions.html", context={"title": "Questions", "questions": queryset})
    except Exception as e:
        print(e)
        return HttpResponseServerError()
