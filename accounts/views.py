from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm

def user_login(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('user-home')

    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('user-home')

    else:
        form = UserLoginForm()

    context['user_login'] = form
    return render(request, 'user/login.html', context)

def user_register(request):
    context = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
        else:
            context['user_register'] = form
    else:
        form = UserRegistrationForm()
        context['user_register'] = form
    return render(request, 'user/register.html', context)

def user_home(request):
    return render(request, 'user/home.html')

def user_logout(request):
    logout(request)
    return redirect('user-login')
