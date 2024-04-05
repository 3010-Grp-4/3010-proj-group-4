from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect

from dashboard import models
from django.urls import reverse

from .models import Faculty
from django.db.models import Q


# Create your views here.


def home(request):
    return render(request, 'dashboard/index.html')


# def about(request):
#     return render(request, 'dashboard/about.html')

def faculty(request):
    faculties = Faculty.objects.all()

    # Start with an empty Q object
    query = Q()

    # Retrieve query parameters
    name = request.GET.get('name')
    email = request.GET.get('email')
    rank = request.GET.get('rank')
    phone = request.GET.get('phone')
    office = request.GET.get('office')
    research_interest = request.GET.get('research_interest')
    remarks = request.GET.get('remarks')

    # Dynamically build the query based on the presence of parameters
    if name:
        query &= Q(user__username__icontains=name)
    if email:
        query &= Q(email__icontains=email)
    if rank:
        query &= Q(position__icontains=rank)
    if phone:
        query &= Q(phone__icontains=phone)
    if office:
        query &= Q(office__icontains=office)
    if research_interest:
        query &= Q(research_interest__icontains=research_interest)
    if remarks:
        query &= Q(remarks__icontains=remarks)

    # Apply the constructed query to filter faculties
    faculties = faculties.filter(query)

    context = {
        'faculty': faculties,
    }
    return render(request, 'dashboard/faculty.html', context)


# def students(request):
#     return render(request, 'dashboard/students.html')

def courses(request):
    return render(request, 'dashboard/courses.html')


def fte(request):
    return render(request, 'dashboard/fte.html')


def profile(request):
    return render(request, 'dashboard/profile.html')


def table(request):
    return render(request, 'dashboard/table.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            print('Successful Login ! ')
            messages.success(request, 'Successful Login ! ')
            return redirect('dashboard:faculty')
        else:
            messages.success(request, 'ERROR: No username or password, please try again..')
            return render(request, 'dashboard/login.html', {})
    else:
        return render(request, 'dashboard/login.html', {})


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User was just registered')
            return redirect('dashboard:login')

    return render(request, 'dashboard/register.html')


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    print('Logout was Successful !: Thanks for joining the resistance...')
    messages.success(request, 'Logout was Successful !')
    return render(request, 'dashboard/faculty.html')

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             print('User was just registered')
#             return render(request, 'dashboard/login.html')
#     return render(request, 'dashboard/register.html')
