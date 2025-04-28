from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Group, Message, Profile, Workout, MealLog, Badge, UserBadge
from .forms import UserProfileForm, WorkoutLogForm, MealLogForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm,  GroupForm, ProfileForm
from .utils import check_and_award_badges, ensure_badges_exist

################################## Front end applications #############################
def index(request):
    return render(request, "pages/index.html") # Render the index.html template

@login_required
def dashboard(request):
    # Fetch the logged meals and workouts for the current user
    meals = MealLog.objects.filter(user=request.user)
    workouts = Workout.objects.filter(user=request.user)
    
    return render(request, "dashboard.html", {'meals': meals, 'workouts': workouts})

#################################### User Authentication #############################
# User Registration View
def register(request):
    if request.method == 'POST': # If the form has been submitted
        form = CustomUserCreationForm(request.POST) # Create a form instance with the submitted data
        if form.is_valid(): # If form is valid, log in and save the user
            user = form.save() 
            login(request, user) 
            return redirect('dashboard') 
    else:
        form = CustomUserCreationForm() # Create an instance of the form
    return render(request, 'account/register.html', {'form': form}) # Render the register.html template

# User Login View
def login_view(request):
    if request.method == 'POST': # If the form has been submitted
        form = CustomAuthenticationForm(request, data=request.POST) # Create a form instance with the submitted data
        if form.is_valid(): # If form is valid, get the user and log them in
            user = form.get_user() 
            login(request, user) 
            return redirect('dashboard') 
    else: 
        form = CustomAuthenticationForm() # Create an instance of the form
    return render(request, 'account/login.html', {'form': form}) 

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('account/logout.html')

################################## Fitness Tracking #############################
# Log Workouts
@login_required
def log_workout(request):
    if request.method == "POST":
        form = WorkoutLogForm(request.POST)
        if form.is_valid():     # If the form is valid, save the workout
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('dashboard')
    else:
        form = WorkoutLogForm()

    check_and_award_badges(request.user) # Check and award badges after logging a workout

    return render(request, 'logs/log_workout.html', {'form': form})

# Log Meals
@login_required
def log_meal(request):
    if request.method == "POST": 
        form = MealLogForm(request.POST)
        if form.is_valid():     # If the form is valid, save the meal
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            return redirect('dashboard')
    else:
        form = MealLogForm()

    ensure_badges_exist() # Ensure badges exist in the database
    check_and_award_badges(request.user) # Check and award badges after joining a group

    return render(request, 'logs/log_meal.html', {'form': form})

# Delete user workouts
@login_required
def delete_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id, user=request.user)
    workout.delete()
    return redirect('dashboard')

# Delete logged meals
@login_required
def delete_meal(request, meal_id):
    meal = MealLog.objects.get(id=meal_id, user=request.user)
    meal.delete()
    return redirect('dashboard')

#################################### Routine Management #############################
@login_required
def routine_view(request): # Routine view for logged meals and workouts
    profile = request.user.profile
    meals = ['Breakfast', 'Lunch', 'Dinner']

    # Handle form submission for profile update
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('routine')
    else:
        form = ProfileForm(instance=profile)

    # Get today's date
    today = timezone.now().date()

    # Filter meals and workouts for today using year, month, and day
    logged_meals = MealLog.objects.filter(user=request.user, 
                                          date__year=today.year,
                                          date__month=today.month,
                                          date__day=today.day)
    
    logged_workouts = Workout.objects.filter(user=request.user,
                                                date__year=today.year,
                                                date__month=today.month,
                                                date__day=today.day)

    # Calculate total calories consumed
    total_calories = sum(meal.calories for meal in logged_meals)

    # Calculate total calories burned
    total_calories_burned = sum(workout.calories_burned for workout in logged_workouts)

    # Define user goals
    calorie_goal = profile.calorie_goal if hasattr(profile, 'calorie_goal') else 2000
    workout_goal = 3  # Example goal of 3 workouts per day

    # Calculate progress percentages
    calorie_percent = min((total_calories / calorie_goal) * 100, 100)
    calories_burned_percent = min((total_calories_burned / calorie_goal) * 100, 100)  
    workout_percent = min((len(logged_workouts) / workout_goal) * 100, 100)

    context = { # Pass the context, including the form and logged meals/workouts
        'profile_form': form,
        'meals': meals,
        'total_calories': total_calories,
        'total_calories_burned': total_calories_burned,
        'calorie_goal': calorie_goal,
        'calorie_percent': calorie_percent,
        'calories_burned_percent': calories_burned_percent,  # Add this to context
        'workout_percent': workout_percent,
        'logged_meals': logged_meals,
        'logged_workouts': logged_workouts
    }

    return render(request, 'logs/routine.html', context)

################################## User Profile Management #############################
# Profile Management View
@login_required
def profile(request):
    if request.method == 'POST': # If the form has been submitted, create a form instance with the submitted data
        form = UserProfileForm(request.POST, instance=request.user) 
        if form.is_valid(): 
            form.save() 
            return redirect('dashboard') # Redirect to dashboard if profile is updated
    else:
        form = UserProfileForm(instance=request.user) 
    return render(request, 'account/profile.html')

@login_required # Ensure the user is logged in to delete their account
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log them out before deleting
        user.delete()
        return render(request, 'account/account_deleted.html') 
    return redirect('profile')

# Profile View for logged-in users
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST': # If the form has been submitted, create a form instance with the submitted data
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'account/profile.html', {
        'profile_form': form,
    })


########################### Group Management #######################################
@login_required
def group_list(request): # List all groups and fetch
    groups = Group.objects.all() 
    return render(request, 'groups/group_list.html', {'groups': groups}) 

# Create Group View
@login_required
def group_create(request): 
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(request.user)  # Creator joins automatically
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'groups/group_form.html', {'form': form}) 

# Group Detail View
@login_required
def group_detail(request, group_id): # View group details and messages
    group = get_object_or_404(Group, id=group_id)
    messages = Message.objects.filter(group=group).order_by('timestamp')

    if request.method == 'POST': # If the form has been submitted, get message content
        content = request.POST.get('message') 
        if content:
            Message.objects.create(group=group, user=request.user, content=content)
            return redirect('group_detail', group_id=group.id)

    return render(request, 'groups/group_detail.html', { # Render the group detail template
        'group': group,
        'messages': messages
    })

@login_required # Ensure the user is logged in to join a group
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.add(request.user)

    ensure_badges_exist() # Ensure badges exist in the database
    check_and_award_badges(request.user) # Check and award badges after joining a group

    return redirect('group_detail', group_id=group.id)

@login_required # Ensure the user is logged in to leave a group
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.remove(request.user)
    return redirect('group_list')

def group_main(request): # Main view for group management
    return render(request, 'groups/group_main.html')

############################### User Awareness views #######################################
# Pricing view page
def pricing_view(request):
    return render(request, 'pages/pricing.html')

# Conservation View
def conservation_view(request): # Define grid rows and columns for the conservation page
    grid_rows = [1, 2, 3] 
    grid_cols = [1, 2, 3]
    return render(request, 'pages/conservation.html', {
        'grid_rows': grid_rows,
        'grid_cols': grid_cols,
    })


############################# Challenge and Badges Management ###############################
@login_required
def challenges_and_badges(request): 
    user_badges = UserBadge.objects.filter(user=request.user) # Fetch badges for the logged-in user
    return render(request, 'pages/challenges.html', {'user_badges': user_badges})
