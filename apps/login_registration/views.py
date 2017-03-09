from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User
import types

# displays a page where user can either register or log in
def index(request):
    return render(request, 'login_registration/index.html')

# registers user name, email, and password if all information is valid
def register(request):
    if request.method != 'POST':
        return redirect(reverse('travel_buddy:registration_page'))
    else:
        user = User.objects.register(request.POST)
        if isinstance(user, types.ListType):
            for error in user:
                messages.error(request, error)
            return redirect(reverse('travel_buddy:registration_page'))
        else:
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            messages.success(request, "Successfully registered!")
            return redirect(reverse('travel_buddy:travels'))

# logs in user if user information is valid and saves information into a session
def login(request):
    if request.method != 'POST':
        return redirect(reverse('travel_buddy:login_page'))
    else:
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid Username or Password!")
            return redirect(reverse('travel_buddy:login_page'))
        else:
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            messages.success(request, "Successfully logged in!")
            return redirect(reverse('travel_buddy:travels'))

# logs out a user and deletes session containing user information
def logout(request):
    User.objects.logout(request.session['user_id'])
    return redirect(reverse('travel_buddy:index'))
