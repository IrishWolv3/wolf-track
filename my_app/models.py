from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.contrib.auth import get_user_model

####### Basic User Profile and Fitness Tracking Models ########
######### User Management #########

# Custom User Model
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True) # Bio attribute
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile picture attribute for uploading images

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True) # Many-to-many relationship with Group model
    user_permissions = models.ManyToManyField(Permission, related_name="custom_permission_set", blank=True) # Many-to-many relationship with Permission model


# User profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    fitness_goal = models.TextField(blank=True, help_text="User's fitness objectives")

    def __str__(self):
        return self.user.username

User = get_user_model()
def default_user():
    first_user = User.objects.first()
    return first_user.id if first_user else None  # Ensure it returns None if no user exists

######################## Workout & Meal logging models #######################
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    workout_type = models.CharField(max_length=100, help_text="E.g., Running, Weight Training")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    calories_burned = models.PositiveIntegerField(help_text="Estimated calories burned")

    def __str__(self):
        return f"{self.user.username} - {self.workout_type} on {self.date}"

# Meal logging model
class MealLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    meal_type = models.CharField(max_length=50, help_text="Breakfast, Lunch, Dinner, Snack")
    calories = models.PositiveIntegerField(help_text="Total calorie intake")

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} on {self.date}"
    
############################## Wolf Pack Management #################################
# Group Model
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True) # Unique name for the group
    description = models.TextField(blank=True) # Optional description
    created_at = models.DateTimeField(auto_now_add=True) # Creation timestamp
    members = models.ManyToManyField(User, related_name='custom_groups', blank=True) # Many-to-many relationship with User

    def __str__(self): # String representation
        return self.name
    
# For chatting in groups   
class Message(models.Model): # Group chat message model
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}: {self.content[:20]}"