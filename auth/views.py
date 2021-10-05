from auth.forms import SignUpForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.


def signUpUser(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Create account success")
            return redirect('signInUser')
        else:
            messages.success(request, "Create account fail")
    return render(request, "auth/sign-up.html", {'form': form})


def signInUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signUp')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/sign-in.html', {'form': form})


def signOutUser(request):
    logout(request)
    return redirect('signInUser')
