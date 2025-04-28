from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Workout, MealLog, Group, Profile

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

# Profile form (for personalized fitness info)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['weight', 'height_feet', 'height_inches', 'age', 'desired_weight']
        widgets = {
            'weight': forms.NumberInput(attrs={'placeholder': 'Your current weight (kg)'}),
            'height_feet': forms.NumberInput(attrs={'placeholder': 'Feet (e.g., 5)'}),
            'height_inches': forms.NumberInput(attrs={'placeholder': 'Inches (e.g., 10)'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Your age'}),
            'desired_weight': forms.NumberInput(attrs={'placeholder': 'Target weight (kg)'})
        }



# Workout Log Form
class WorkoutLogForm(forms.ModelForm):
    class Meta: # Meta class to define the model and fields for the form
        model = Workout
        fields = ['workout_type', 'duration', 'sets', 'reps', 'calories_burned']
        widgets = { # Widgets to customize the appearance of the form fields
            'workout_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Push Ups'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 12'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 250'}),
        }

# Meal Log Form
class MealLogForm(forms.ModelForm):
    class Meta: # Meta class to define the model and fields for the form
        model = MealLog
        fields = ['meal_name', 'meal_type', 'quantity', 'calories']
        widgets = { # Widgets to customize the appearance of the form fields
            'meal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Chicken Salad'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 200g'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 350'}),
        }

# Group form (for group management)
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']