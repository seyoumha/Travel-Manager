from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import bcrypt

def login(request):
    return render(request, 'travel_buddy/login_form.html')
def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        password = request.POST['password'].encode()
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User.objects.create(name= request.POST['name'], username= request.POST['username'], password = hashed)
        request.session['id'] = user.id
        return redirect('/travel')


def signin(request):
    errors = User.objects.password_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        username = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username = username):
            user = User.objects.filter(username = username)
        else:
            messages.error(request, "User does not exist. Please try again or create an account")
            return redirect('/main')
        u_password = user.first().password
        if user.count() > 0 and user.first().username == username and bcrypt.checkpw(password.encode(), u_password.encode()):
            request.session['id'] = user.first().id
            return redirect('/travel')
        else:
            messages.error(request, "User name and password does not match")
            return redirect('/main')
def logout(request):
    id = request.session['id']
    del request.session['id'] 
    return redirect('/main')

def travel(request):
    user = User.objects.get(id=request.session['id'])
    user_trips = []
    for t in user.traveler.all():
        user_trips.append(t.travler.id)
    all_travels = Travel.objects.all()
    trips = Trips.objects.all()
    return render(request,'travel_buddy/index.html',{'user': user, 'all_travels':all_travels, 'user_trips': user_trips, 'trips': trips})

def process_travel(request, id):
    errors = Travel.objects.travel_add_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/travel/add')
    else:
        Travel.objects.create(destination= request.POST['destination'], plan = request.POST['plan'], start_date = request.POST['from'], end_date= request.POST['to'], user_id = request.session['id'])
        return redirect('/travel')

def add_travel(request):
    return render(request, 'travel_buddy/travel.html')
def join_travel(request):
    Trips.objects.create(user_id = request.session['id'], travler_id = request.POST['id'])
    return redirect('/travel')
def show_travel(request, id):
    travel = Travel.objects.get(id = id)
    trips = Trips.objects.all()
    return render(request, 'travel_buddy/show.html',{'travel': travel, 'trips': trips} )
