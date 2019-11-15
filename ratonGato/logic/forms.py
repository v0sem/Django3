from django import forms
from datamodel.models import Move, Game
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation, authenticate

from logic import tests_services


class loginForm(AuthenticationForm):


    def is_valid(self):

        name = self.data['username']
        passw = self.data['password']

        if not User.objects.filter(username=name).exists():
            self.add_error(None, tests_services.SERVICE_DEF[tests_services.LOGIN_ERROR]['pattern'])
            return False
        
        if not authenticate(username=name, password=passw):
            self.add_error(None, tests_services.SERVICE_DEF[tests_services.LOGIN_ERROR]['pattern'])
            return False
        
        return super(loginForm, self).is_valid()
    

    class Meta:
        model = User
        fields = ('username', 'password')