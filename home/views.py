from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UserLevelRecordForm
from .models import Level, User_Level_Record
from django.views.decorators.csrf import csrf_protect

def home(request):
    levels = Level.objects.all()
    records = []
    user = request.user
    for level in levels:
        if user.is_authenticated:
            try:
                record = User_Level_Record.objects.get(level=level, user=user)
                records.append({'level': level, 'record': record})
            except User_Level_Record.DoesNotExist:
                records.append({'level': level, 'record': None})
        else:
            records.append({'level': level, 'record': None})
    context = {
        'records':records
    }
    return render(request, 'home.html', context)

def play(request, level_num=None):
    # Get the level object that the score was submitted for
    level = Level.objects.get(level_number=level_num)
    
    # Get the user object for the logged-in user
    user = request.user
    
    # If the user is not logged in, don't update the models
    if not user.is_authenticated:
        if request.method == 'POST':
            print("not logged in")
            return redirect('recap')
        return render(request, 'play.html', {'level': level})
    
    # If this is a POST request, validate and save the new score
    if request.method == 'POST':
        form = UserLevelRecordForm(user=user, level=level, data=request.POST)
        if form.is_valid():
            previous_records = User_Level_Record.objects.filter(user=form.user, level=form.level)
            if previous_records:
                previous_records.delete()
                print('deleting previous records')
            else:
                print('no records to delete')
            print(f'score: {form.score} || user: {form.user} || level: {form.level}')
            print('saving new rocord')
            record = form.save(commit=False)
            record.user = form.user
            record.level = form.level
            record.score = form.score
            record.save()
        return redirect('recap')
    
    # If this is a GET request, display the form
    form = UserLevelRecordForm(level=level, user=user)
    context = {'form': form, 'level': level}
    return render(request, 'play.html', context)
    
def recap(request):
    return render(request, 'recap.html', {})
    
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