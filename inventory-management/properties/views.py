from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserRegistrationForm
from django.contrib.auth.models import Group


def home(request):
    return HttpResponse("Hello")


def signup(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Ensure the "Property Owners" group exists
            group, created = Group.objects.get_or_create(name="Property Owners")
            user.groups.add(group)
            
            messages.success(request, 'Your account has been created! You are now a Property Owner.')
            return redirect('home')  # Redirect to the home page
        else:
            print(form.errors)  # Debugging line to print form errors
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'signup.html', {'form': form})
