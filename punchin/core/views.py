from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .forms.user_create_form import CustomUserCreationForm


def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('home')
        else:
            print("'invalid login' error message", user)
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        mutable_post = request.POST.copy()
        mutable_post['email'] = request.POST['username']
        form = CustomUserCreationForm(mutable_post)
        if form.is_valid():
            form.save()
            # Redirect to a success page
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
