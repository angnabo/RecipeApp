from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from recipeApp.users.forms import UserForm


def index(request):
    return render('users/login.html')


def signUp(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

def logIn(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.

    else:
        #asdasd


def logout_view(request):
    logout(request)