from django.contrib import admin
from .models import UserProfile, Workout, MealLog

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Workout)
admin.site.register(MealLog)