from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Trip, Traveler
from ..login_registration.models import User
import types

# displays a login and registration page
def index(request):
    return render(request, 'travel_buddy/index.html')

def registration_page(request):
    return render(request, 'travel_buddy/registration_page.html')

def login_page(request):
    return render(request, 'travel_buddy/login_page.html')

# displays a dashboard page displaying current user's travel plans along with
# other users' travel plans
def travels(request):
    try:
        trips = Trip.objects.filter(planner=request.session['user_id']).order_by('start_date')|\
            Trip.objects.filter(travelers=request.session['user_id']).order_by('start_date')
        other_trips = Trip.objects.all().exclude(planner=request.session['user_id'])
    except Trip.DoesNotExist:
        trips = None
        other_trips = None
    context = {
        'trips': trips,
        'other_trips': other_trips
    }
    return render(request, 'travel_buddy/travels2.html', context)

# displays a page specific to one travel destination
# shows other users travelling on this specific trip
def destination(request, id):
    trip = Trip.objects.get(id=id)
    planner = User.objects.get(user=trip.planner.id)
    context = {
        'trip': trip,
        'travelers': Traveler.objects.filter(trip=trip).exclude(user=planner)
    }
    return render(request, 'travel_buddy/destination2.html', context)

# displays a page containing a form that allows the user to add a new travel plan
def add(request):
    return render(request, 'travel_buddy/add2.html')

# creates a new travel plan for the user
def create(request):
    if request.method != 'POST':
        return redirect(reverse('travel_buddy:add'))
    else:
        trip = Trip.objects.add_trip(request.POST, request.session['user_id'])
        if isinstance(trip, types.ListType):
            for error in trip:
                messages.error(request, error)
            return redirect(reverse('travel_buddy:add'))
        else:
            return redirect(reverse('travel_buddy:travels'))

# allows the user to join other users' travel plans
def join(request, id):
    Trip.objects.join_trip(id, request.session['user_id'], request.session['first_name'], request.session['last_name'])
    return redirect(reverse('travel_buddy:travels'))
