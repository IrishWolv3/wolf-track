from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Workout, MealLog

# User Registration Form
class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150) #
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['age', 'height', 'weight', 'fitness_goal']

    def clean(self): 
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        profile = super().save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return user

# Workout Log Form
class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['workout_type', 'duration', 'calories_burned']
        widgets = {
            'workout_type': forms.TextInput(attrs={'placeholder': 'E.g., Running, Weight Training'}),
            'duration': forms.NumberInput(attrs={'placeholder': 'Minutes'}),
            'calories_burned': forms.NumberInput(attrs={'placeholder': 'Calories Burned'}),
        }

# Meal Log Form
class MealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['meal_type', 'calories']
        widgets = {
            'meal_type': forms.TextInput(attrs={'placeholder': 'E.g., Breakfast, Lunch'}),
            'calories': forms.NumberInput(attrs={'placeholder': 'Calories'}),
        }