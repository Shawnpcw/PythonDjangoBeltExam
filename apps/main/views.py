from django.shortcuts import render, HttpResponse, redirect
from apps.main.models import *
from django.contrib import messages

def index(request):
    
    if 'first_name' not in request.session:
        request.session['first_name'] = ''
    if 'last_name' not in request.session:
        request.session['last_name'] = ''
    if 'email' not in request.session:
        request.session['email'] = ''        
    if 'current_first_name' not in request.session:
        request.session['current_first_name'] = ''         
    return render(request,'main/index.html')
def create_user(request):

    response = User.objects.basic_validator(request.POST)
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request,error)
        print(messages.error)
        return redirect('main:index')
        
    else:
        request.session['user_id'] = response['user_id']      
        return redirect('/travels')     
def login_user(request):
    response = User.objects.login_validator(request.POST)
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request,error)
        return redirect('main:index')
    else:
        request.session['user_id'] = response['user_id']      
        return redirect('main:travel')  
def travel(request):
    if 'user_id' not in request.session:
        return redirect('main:index')
    request.session['current_first_name'] = User.objects.get(id=request.session['user_id']).first_name
    # p =User.objects.get(id=request.session['user_id']).your_trip.all())
    allTrips= Trip.objects.all().difference(User.objects.get(id=request.session['user_id']).your_trip.all())
    myTrips =User.objects.get(id=request.session['user_id']).your_trip.all()
    return render(request, 'main/travels.html',{'allTrips':allTrips,'myTrips':myTrips})

def logout(request):
    del request.session['user_id']
    
    return redirect('main:index')
def create(request):
    if 'user_id' not in request.session:
        return redirect('main:index')

    return render(request, 'main/create.html')
def createTrip(request):
    userid= request.session['user_id']
    response = Trip.objects.trip_validator(request.POST,userid)
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request,error)
        return redirect('main:create')
    else:  
        return redirect('main:travel')  
def view(request,id):
    if 'user_id' not in request.session:
        return redirect('main:index')
    currentUser=User.objects.get(id=request.session['user_id'])
    tripInfo = Trip.objects.get(id=id)
    attendees= Trip.objects.get(id=id).trip_attendee.exclude(id =currentUser.id)
    print(attendees)
    return render(request, 'main/view.html',{'tripInfo':tripInfo,'attendees':attendees})
def join_trip(request,id):
    
    User.objects.get(id=request.session['user_id']).your_trip.add(Trip.objects.get(id=id))
    return redirect('main:travel')
def leave_trip(request,id):
    
    User.objects.get(id=request.session['user_id']).your_trip.remove(Trip.objects.get(id=id))
    return redirect('main:travel')
def delete_trip(request,id):
    p= Trip.objects.get(id = id)
    p.delete()
    return redirect('main:travel')

