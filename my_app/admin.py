from django.contrib import admin
from .models import UserProfile, Workout, MealLog, Challenge, Badge, UserBadge

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Workout)
admin.site.register(MealLog)
admin.site.register(Badge)
admin.site.register(UserBadge)