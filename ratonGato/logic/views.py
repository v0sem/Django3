from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as djangologin, logout as djangologout
from datamodel.models import Game, Move, Counter, GameStatus

from datamodel import constants
from logic.forms import loginForm, SignupForm

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
            request.session['counter'] = 0
            request.session.modified = True
            return redirect('index')
        

    return render(request, "mouse_cat/login.html", {'user_form': form})


@login_required
def logout(request):
    djangologout(request)
    request.session['counter'] = 0
    return render(request, "mouse_cat/logout.html")

@anonymous_required
def signup(request):
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            user.save()
            djangologin(request, user)
            request.session['counter'] = 0
            form = None


    return render(request, "mouse_cat/signup.html", {'user_form': form})

def counter(request):

    if 'counter' in request.session:
        request.session['counter'] += 1
    else:
        request.session['counter'] = 1

    counter_global = Counter.objects.inc()

    return render(request, "mouse_cat/counter.html", {'counter_session': request.session['counter'],
                                                    'counter_global': counter_global})


@login_required
def create_game(request):

    user = request.user
    game = Game(cat_user=user)
    game.save()

    return render(request, "mouse_cat/new_game.html", {'game': game})

@login_required
def select_game(request, game_id=-1):
    user = request.user

    if game_id == -1:
        context_dict = {}
        as_cat = Game.objects.filter(cat_user=user, status=GameStatus.ACTIVE)
        if as_cat:
            context_dict['as_cat'] = as_cat

        as_mouse = Game.objects.filter(
            mouse_user=user, status=GameStatus.ACTIVE)
        if as_mouse:
            context_dict['as_mouse'] = as_mouse

        return render(request, "mouse_cat/select_game.html", context_dict)
    else:
        game = Game.objects.filter(id=game_id).first()
        if not game or game.status != GameStatus.ACTIVE:
            raise Http404
        else:
            if game.cat_user == user or game.mouse_user == user:

                request.session['game_id'] = game.id
                return redirect(reverse('show_game'))

            else:
                raise Http404

def show_game(request):
    return render(request, "mouse_cat/game.html")

@login_required
def join_game(request):

    user = request.user
    available_games = Game.objects.exclude(cat_user=user).filter(mouse_user__isnull=True).order_by('-id')

    if not available_games:
        context_dict = {}
        context_dict[constants.ERROR_MESSAGE_ID] = """No hay juegos disponibles a los que unirse."""
        return render(request, "mouse_cat/join_game.html", context_dict)
    else:
        game = available_games.first()
        game.mouse_user = user
        game.save()
        return render(request, "mouse_cat/join_game.html", {'game': game})

def move(request):
    return render(request, reverse("show_game"))