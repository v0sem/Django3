from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, reverse

from datamodel import constants


def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            return HttpResponseForbidden(
                errorHTTP(request, exception="Action restricted to anonymous users"))
        else:
            return f(request)
    return wrapped


def errorHTTP(request, exception=None):
    context_dict = {}
    context_dict[constants.ERROR_MESSAGE_ID] = exception
    return render(request, "mouse_cat/error.html", context_dict)


def index(request):
    return render(request, "mouse_cat/index.html")

def login(request):
    return render(request, "mouse_cat/login.html")

def logout(request):
    return render(request, "mouse_cat/logout.html")

def signup(request):
    return render(request, "mouse_cat/signup.html")

def counter(request):
    return render(request, "mouse_cat/counter.html")

def create_game(request):
    return render(request, "mouse_cat/new_game.html")

def select_game(request):
    return render(request, "mouse_cat/select_game.html")

def show_game(request):
    return render(request, "mouse_cat/game.html")

def join_game(request):
    return render(request, reverse("show_game"))

def move(request):
    return render(request, reverse("show_game"))