from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def match(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Game Match</h1>")
