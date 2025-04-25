from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Workout, MealLog, Group

# User Registration Form
# Custom user creation form (for registration)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")  # Adding email field
    first_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your first name.") # Adding first name field
    last_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your last name.") # Adding last name field

    class Meta:
        model = User # Using Django's built-in User model
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2'] # Fields included in the form

    # Custom clean method to check if email already exists
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists(): # If it exists, raise a validation error
            raise forms.ValidationError("A user with this email already exists.")
        return email

# Custom authentication form (for login)
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) # Adding class to username field
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})) # Adding class to password fieldS

# User profile form (for profile management)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

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

# Group form (for group management)
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']