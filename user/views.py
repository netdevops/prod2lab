from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib import messages


def user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/user/login/')


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    elif request.method == "GET":
        return render(request, 'user/login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')

    messages.warning(request, 'invalid username and/or password')
    return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
