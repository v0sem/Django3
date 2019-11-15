from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as djangologin, logout as djangologout

from datamodel import constants
from logic.forms import loginForm

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

@anonymous_required
def login(request):

    form = loginForm()    

    if request.method == 'POST':
        form = loginForm(data=request.POST)

        if form.is_valid():
            
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            
            djangologin(request, user)
            request.session.modified = True
            return redirect('index')
        
        return render(request, "mouse_cat/login.html", {'user_form': form})

    return render(request, "mouse_cat/login.html", {'user_form': form})


def logout(request):
    djangologout(request)
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