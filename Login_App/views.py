from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Login_App.forms import SignUpForm, UserProfileChangeForm, ProfilePicForm

def sign_up(request):
    form = SignUpForm()
    registered = False  # Corrected variable name
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    context = {'form': form, 'registered': registered}  # Corrected variable name
    return render(request, 'Login_App/signup.html', context=context)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            
    return render(request, 'Login_App/login.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def profile (request):
    return render(request, 'Login_App/profile.html', context={})

@login_required
def user_change(request):
    current_user = request.user
    
    if request.method == 'POST':
        form = UserProfileChangeForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page after successful update
    else:
        form = UserProfileChangeForm(instance=current_user)

    return render(request, 'Login_App/change_profile.html', context={'form': form})
@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    
    if request.method == 'POST':  # Correctly check the request method
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True

    return render(request, 'Login_App/pass_change.html', context={'form': form, 'changed': changed})

@login_required
def add_profile_pic(request):
    try:
        # Try to get the existing UserProfile
        user_profile = request.user.user_profile
    except user_profile.DoesNotExist:
        # If no UserProfile exists, initialize user_profile as None
        user_profile = None

    if request.method == "POST":
        form = ProfilePicForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile_pic = form.save(commit=False)
            profile_pic.user = request.user
            profile_pic.save()
            return HttpResponseRedirect(reverse('Login_App:profile'))
    else:
        form = ProfilePicForm(instance=user_profile)

    return render(request, 'Login_App/pro_pic_add.html', {'form': form})