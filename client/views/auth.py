from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from client.forms.auth import ClientLoginForm, ClientRegistrationForm
from core.models.user import User
from core.decorators import client_required

def client_login_view(request):
    """
    Client login view.
    """
    if request.method == 'POST':
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_client():
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('client_dashboard')
            else:
                messages.error(request, "Invalid email or password, or you don't have client privileges.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = ClientLoginForm()
    
    return render(request, 'shared/auth/login.html', {'form': form})

def client_register_view(request):
    """
    Client registration view.
    """
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}. You can now log in.")
            return redirect('login')
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'shared/auth/register.html', {'form': form})

@login_required
def client_logout_view(request):
    """Logout view for client users."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
