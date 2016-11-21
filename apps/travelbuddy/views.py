from django.shortcuts import render, redirect
from models import Trip, User
from django.contrib import messages
from django.db.models import Q
def session_check(request):
  if 'user' in request.session:
      return True
  else:
      return False

def index(request):
    print 
    if not session_check(request):
        return redirect('login:index')

    context = {
        "all_trips": Trip.objects.exclude(Q(travelers__name=request.session['user']['name']) | Q(planner__name=request.session['user']['name'])),
        "user_trips": Trip.objects.filter(Q(travelers__name=request.session['user']['name']) | Q(planner__name=request.session['user']['name']))
    }
    
    return render(request, 'travelbuddy/index.html', context)
def create_trip_page(request):
    return render(request, 'travelbuddy/create_trip.html')

def add_trip(request):
    if session_check(request):
        errors = Trip.objects.make_trip(request)

        if errors:
            print_errors(request,errors)
            return redirect('travel:create_trip')

        return redirect('travel:index')
        
    return redirect('login:index')


def show_trip(request, id):
    if session_check(request):
        context = {
            'trip': Trip.objects.get(id=id),
            'travelers': User.objects.filter(user_trips=id)
        }

        return render(request, 'travelbuddy/show_trip.html', context)

    return redirect('login:index')

def join_trip(request, id):
    user = User.objects.get(id=request.session['user']['user_id'])
    trip = Trip.objects.get(id=id)
    trip.travelers.add(user)
    return redirect('travel:index')

def print_errors(request, error_list):
    for error in error_list:
        messages.add_message(request, messages.INFO, error)