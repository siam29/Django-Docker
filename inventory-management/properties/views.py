from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm

def home(request):
    return HttpResponse("Welcome to the Home Page!")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signup_success(request):
    return render(request, 'signup_success.html')