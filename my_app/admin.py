from django.contrib import admin
from .models import UserProfile, Workout, MealLog, Challenge, Badge, UserBadge

# Register your models here.

admin.site.register(UserProfile) # This is the user profile model, which extends the default User model.
admin.site.register(Workout) # This is the workout model, which tracks user workouts.
admin.site.register(MealLog) # This is the meal log model, which tracks user meals.
admin.site.register(Badge) # This is the badge model, which represents badges that users can earn.
admin.site.register(UserBadge) # This is the user badge model, which tracks which badges a user has earned.