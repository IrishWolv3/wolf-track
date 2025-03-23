from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Workout, MealLog
from .forms import UserProfileForm, WorkoutForm, MealLogForm
from django.contrib import messages

# Create your views here.

# Home Page
def index(request):
    return render(request, 'my_app/index.html')

# User Dashboard
@login_required
def dashboard(request):
    workouts = Workout.objects.filter(user=request.user)
    meals = MealLog.objects.filter(user=request.user)
    return render(request, 'my_app/dashboard.html', {'workouts': workouts, 'meals': meals})

# User Registration
def register(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserProfileForm()
    return render(request, 'my_app/register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'my_app/login.html')

# User Logout
def user_logout(request):
    logout(request)
    return redirect('index')

# Log Workouts
@login_required
def log_workout(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('dashboard')
    else:
        form = WorkoutForm()
    return render(request, 'my_app/log_workout.html', {'form': form})

# Log Meals
@login_required
def log_meal(request):
    if request.method == "POST":
        form = MealLogForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('dashboard')
    else:
        form = MealLogForm()
    return render(request, 'my_app/log_meal.html', {'form': form})