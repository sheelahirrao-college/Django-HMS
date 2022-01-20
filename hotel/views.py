from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import HotelRegistrationForm, HotelLoginForm

def hotel_home(request):
    return render(request, 'hotel/home.html')

def hotel_login(request):

    context = {}

    hotel = request.user
    if hotel.is_authenticated:
        return redirect('hotel-home')

    if request.POST:
        form = HotelLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            hotel = authenticate(username=username, password=password)

            if hotel:
                login(request, hotel)
                return redirect('hotel-home')

    else:
        form = HotelLoginForm()

    context['hotel_login'] = form
    return render(request, 'hotel/login.html', context)

def hotel_register(request):
    context = {}
    if request.POST:
        form = HotelRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel-login')
        else:
            context['hotel_register'] = form
    else:
        form = HotelRegistrationForm()
        context['hotel_register'] = form
    return render(request, 'hotel/register.html', context)

def hotel_logout(request):
    logout(request)
    return redirect('hotel-login')