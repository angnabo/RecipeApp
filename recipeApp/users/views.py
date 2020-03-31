from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from RecipeApp.recipeApp.users.factories import ProfileFactory
from RecipeApp.recipeApp.users.forms import UserLoginForm, UserSignupForm, UserProfileForm
from RecipeApp.recipeApp.users.models import Profile
from RecipeApp.recipeApp.utils import email_sender


def index(request):
    form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def edit_profile(request):
    profile_object = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile_object)
        if form.is_valid():
            form.save()
            return redirect('recipes:index')
        else:
            return render(request, 'users/profile.html', {'form': form})
    else:
        form = UserProfileForm(request.POST or None, instance=profile_object)
    return render(request, 'users/profile.html', {'form': form})


@login_required(login_url='users:login')
def profile(request):
    try:
        profile_object = Profile.objects.get(user_id=request.user.id)
    except Profile.DoesNotExist:
        new_profile = ProfileFactory.create(request.user)
        new_profile.save()
        profile_object = new_profile

    form = UserProfileForm(request.POST or None, instance=profile_object)
    return render(request, 'users/profile.html', {'profile': profile_object, 'form': form})


def signUp(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            new_profile = ProfileFactory.create(user)
            new_profile.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            # TODO: get the site url
            # send email
            subject = 'You received a comment on your recipe!'
            try:
                template = render_to_string("emails/signup_email.html",
                                            {'url': 'url', 'username': user.get_full_name()})
                email_sender.send_email([user.email], subject, template)
            except Exception as e:
                print(e)
            return redirect('recipes:index')
    else:
        form = UserSignupForm()
    return render(request, 'users/signup.html', {'form': form})


def logIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes:index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')
