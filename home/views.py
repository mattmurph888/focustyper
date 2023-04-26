from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Level, User_Level_Record

def home(request):
    levels = Level.objects.all()
    context = {'levels': levels}
    return render(request, 'home.html', context)
    
def play(request, level_num=None):
    level = Level.objects.get(level_number = level_num)
    context = {'level': level}
    return render(request, 'play.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, 'Username or Password are incorrect...')
                return redirect('login')
        else:
            context = {}
            return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            context = {'form': form}
            return render(request, 'register.html', context)
    else:
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'register.html', context)