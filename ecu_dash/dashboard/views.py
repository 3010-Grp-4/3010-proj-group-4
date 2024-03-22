from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from dashboard import models
from django.urls import reverse


# Create your views here.


def home(request):
    return render(request, 'dashboard/index.html')


# def about(request):
#     return render(request, 'dashboard/about.html')

def faculty(request):
    current_faculty = models.Faculty.objects.all()
    context = {
        'faculty': current_faculty
    }
    return render(request, 'dashboard/faculty.html', context)


# def students(request):
#     return render(request, 'dashboard/students.html')

def courses(request):
    return render(request, 'dashboard/courses.html')


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
