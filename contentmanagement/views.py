from django.db import connection
from django.http import HttpRequest, HttpResponse, HttpResponseServerError, JsonResponse
from django.shortcuts import render

from .models import Question


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html", context={"title": "Home"})


def questions(request: HttpRequest) -> HttpResponse:
    try:
        queryset = Question.objects.select_related("solution").all()
        return render(request, "questions.html", context={"title": "Questions", "questions": queryset})
    except Exception as e:
        print(e)
        return HttpResponseServerError()


def health_check(request: HttpRequest) -> JsonResponse:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchall()

        return JsonResponse({"status": "ok"}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"status": "error"}, status=500)
