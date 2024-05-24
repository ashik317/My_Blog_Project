from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from Login_App.models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email Address", required=True)

    class Meta:  # Use proper casing for Meta
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileChangeForm(UserChangeForm):  # Renamed the class to avoid confusion
    class Meta:  # Use proper casing for Meta
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class ProfilePicForm(forms.ModelForm):  # Use CamelCase for the class name
    class Meta:  # Meta should be capitalized
        model = UserProfile
        fields = ['profile_pic']