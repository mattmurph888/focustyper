from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    context = {}
    return render(request, 'home.html', context)
    
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