from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from dashboard import models


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


def register_user(request):
    # TODO: Add a check to see if the user is already logged in
    # TODO: VERIFY THAT THE CURRENT BELOW CODE WORKS BEFORE EDITING
    if request.method == 'POST':
        print('POST request received')
        # Get user details from the form
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']

        print(f'\n\n\n\nUsername: {username}')
        print(f'Password: {password}')
        print(f'First Name: {first_name}')
        print(f'Last Name: {last_name}')
        print(f'Email: {email}\n\n\n')

        # Get the user details from the form
        # profile_img_url = request.POST['profile_img_url']
        # account_type = request.POST['account_type']

        # print(f'Profile Image URL: {profile_img_url}')
        # print(f'Account Type: {account_type}')

        profile_img_url = 'https://media.istockphoto.com/id/168415745/photo/black-panther.webp?b=1&s=170667a&w=0&k=20&c=VUXE_4-AEIAJIxRvVjkbENkBfroAXrzaHlUMwE4jR_s='

        # Create the user object
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name

        # Create the user setting / university account for the new user
        settings = models.UserSetting.objects.create(user=user)

        try:
            print('Creating a new user')
            # Save the changes
            user.save()
            # log the user in
            login(request, user)
            print('User was created successfully')
            messages.success(request, 'User was created successfully')

            # Save user settings for the new user
            settings.save()
            print('User setting was created successfully')
            messages.success(request, 'User setting was created successfully')
            return render(request, 'dashboard/faculty.html')  # Redirect to the faculty page
        except Exception as e:
            print(f'An unexpected error occurred: {str(e)}')
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, 'dashboard/register.html')


def login_user(request):
    member = request.user
    context = {'member': member}
    if request.method == 'POST':
        print('POST request received')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('Successful Login!')
            messages.success(request, 'Successful Login!')
            redirect('dashboard/faculty')  # Redirect to the faculty page
        else:
            print('ERROR: No username or password, please try again..')
            messages.error(request, 'ERROR: No username or password, please try again..')
            return render(request, 'dashboard/register.html')  # Correct path to your login template
    else:
        print('ERROR: No username or password, please try again..')
        return render(request, 'dashboard/login.html')  # Correct path to your login template


def logout_user(request):
    # Log the user out
    logout(request)
    print('Logout was Successful !')
    messages.success(request, 'Logout was Successful !')
    return redirect('dashboard:login_user')  # Redirect to the home page
