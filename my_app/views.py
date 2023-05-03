from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UserLevelRecordForm
from .models import Level, User_Level_Record

def home(request):
    levels = Level.objects.all()
    records = []
    user = request.user
    for level in levels:
        if user.is_authenticated:
            # checks if the user has a record for that level already
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
            form = UserLevelRecordForm(user=None, level=level, data=request.POST)
            if form.is_valid():
                # check if we are at the final level, toggles the next level button the on the recap page
                next_level = None
                try:
                    next_level = Level.objects.get(level_number=form.level.level_number+1)
                except Level.DoesNotExist:
                    next_level = None

                context = {
                    'level': form.level,
                    'score': form.score,
                    'accuracy': form.cleaned_data.get('accuracy'),
                    'speed': form.cleaned_data.get('speed'),
                    'saved': False,
                    'next_level': next_level,
                    'logged_in': False,
                }
                return render(request, 'recap.html', context)
        # If this is a GET request, display the form
        form = UserLevelRecordForm(level=level, user=None)
        context = {'form': form, 'level': level}
        return render(request, 'play.html', context)
    
    # If this is a POST request and the user is logged in, validate and save the new score
    if request.method == 'POST':
        form = UserLevelRecordForm(user=user, level=level, data=request.POST)
        if form.is_valid():
            saved = False
            if form.is_high_score():
                saved = True
                previous_records = User_Level_Record.objects.filter(user=form.user, level=form.level)
                if previous_records:
                    previous_records.delete()
                record = form.save(commit=False)
                record.user = form.user
                record.level = form.level
                record.score = form.score
                record.save()

            # check if we are at the final level, toggles the next level button the on the recap page
            next_level = None
            try:
                next_level = Level.objects.get(level_number=form.level.level_number+1)
            except Level.DoesNotExist:
                next_level = None

            context = {
                'level': form.level,
                'score': form.score,
                'accuracy': form.cleaned_data.get('accuracy'),
                'speed': form.cleaned_data.get('speed'),
                'saved': saved,
                'next_level': next_level,
                'logged_in': True,
            }
            return render(request, 'recap.html', context)
    
    # If this is a GET request, display the form
    form = UserLevelRecordForm(level=level, user=user)
    context = {'form': form, 'level': level}
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