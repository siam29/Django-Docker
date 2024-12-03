from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserRegistrationForm

def home(request):
    return HttpResponse("Hello")


def signup(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now a Property Owner.')
            return redirect('home')  # Redirect to the login page
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'signup.html', {'form': form})