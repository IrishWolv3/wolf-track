from django.contrib.auth.models import User
from django.db import models

####### Basic User Profile and Fitness Tracking Models ########
# User profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    fitness_goal = models.TextField(blank=True, help_text="User's fitness objectives")

    def __str__(self):
        return self.user.username

# Workout logging model
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