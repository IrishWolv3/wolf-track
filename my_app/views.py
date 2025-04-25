from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Workout, MealLog, Group, Message
from .forms import UserProfileForm, WorkoutForm, MealLogForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm,  GroupForm

################################## Front end applications #############################
def index(request):
    return render(request, "index.html") # Render the index.html template

@login_required # Ensure the user is logged in to access the dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")  # Redirect if not logged in
    return render(request, "dashboard.html") # Render the dashboard.html template

#################################### User Authentication #############################
# User Registration View
def register(request):
    if request.method == 'POST': # If the form has been submitted
        form = CustomUserCreationForm(request.POST) # Create a form instance with the submitted data
        if form.is_valid(): # If form is valid
            user = form.save() # Save the user to the database
            login(request, user) # Log the user in
            return redirect('dashboard') # Redirect to dashboard if registration is successful
    else:
        form = CustomUserCreationForm() # Create an instance of the form
    return render(request, 'register.html', {'form': form}) # Render the register.html template

# User Login View
def login_view(request):
    if request.method == 'POST': # If the form has been submitted
        form = CustomAuthenticationForm(request, data=request.POST) # Create a form instance with the submitted data
        if form.is_valid(): # If form is valid
            user = form.get_user() # Get the user
            login(request, user) # Log the user in
            return redirect('dashboard') # Redirect to dashboard if login is successful
    else: 
        form = CustomAuthenticationForm() # Create an instance of the form
    return render(request, 'login.html', {'form': form}) # Render the login.html template

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('logout.html')

################################## Fitness Tracking #############################
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
    return render(request, 'log_workout.html', {'form': form})

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
    return render(request, 'log_meal.html', {'form': form})

################################## User Profile Management #############################
# Profile Management View
@login_required
def profile(request):
    if request.method == 'POST': # If the form has been submitted
        form = UserProfileForm(request.POST, instance=request.user) # Create a form instance with the submitted data
        if form.is_valid(): # If form is valid
            form.save() # Save the form
            return redirect('dashboard') # Redirect to dashboard if profile is updated
    else:
        form = UserProfileForm(instance=request.user) # Create an instance of the form
    return render(request, 'profile.html') # Render the profile.html template

@login_required # Ensure the user is logged in to delete their account
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log them out before deleting
        user.delete()
        return render(request, 'account_deleted.html')  # Render a template to confirm account deletion
    return redirect('profile')


########################### Group Management #######################################
@login_required
def group_list(request): # List all groups
    groups = Group.objects.all() # Fetch all groups
    return render(request, 'groups/group_list.html', {'groups': groups}) # Render the group list template

# Create Group View
@login_required
def group_create(request): # Create a new group
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.members.add(request.user)  # Creator joins automatically
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'groups/group_form.html', {'form': form}) # Render the group creation form template

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
    return redirect('group_detail', group_id=group.id)

@login_required # Ensure the user is logged in to leave a group
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.members.remove(request.user)
    return redirect('group_list')

def group_main(request): # Main view for group management
    return render(request, 'group_main.html')

############################### User Awareness views #######################################
# Pricing View
def pricing_view(request):
    return render(request, 'pricing.html')

# Conservation View
def conservation_view(request):
    grid_rows = [1, 2, 3]
    grid_cols = [1, 2, 3]
    return render(request, 'conservation.html', {
        'grid_rows': grid_rows,
        'grid_cols': grid_cols,
    })
