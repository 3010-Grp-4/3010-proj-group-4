from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect

from dashboard import models
from django.urls import reverse

from .models import Faculty, Course
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
        query &= Q(user__first_name__icontains=name) | Q(user__last_name__icontains=name)
    if email:
        query &= Q(user__email__icontains=email)
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

    # Sorting logic
    sort_order = request.GET.get('sort', 'asc')  # Default to ascending order
    if sort_order == 'desc':
        faculties = faculties.order_by('-user')  # Descending sort
    else:
        faculties = faculties.order_by('user')  # Ascending sort

    context = {
        'faculty': faculties,
    }
    return render(request, 'dashboard/faculty.html', context)


# def students(request):
#     return render(request, 'dashboard/students.html')

def courses(request):
    # Start with all courses
    uni_courses = Course.objects.all()

    # Retrieve query parameters for filtering
    course_code = request.GET.get('code')
    course_name = request.GET.get('name')
    course_ch = request.GET.get('ch')
    course_description = request.GET.get('description')

    print("Course code received:", course_code)
    print("Course name received:", course_name)
    print("Course CH received:", course_ch)

    # Filtering based on course name or code
    if course_code:
        uni_courses = uni_courses.filter(course_code__icontains=course_code)
    if course_name:
        uni_courses = uni_courses.filter(course_name__icontains=course_name)
    if course_ch:
        try:
            course_ch_value = float(course_ch)
            uni_courses = uni_courses.filter(course_credit__gte=course_ch_value)
        except ValueError:
            print("Invalid input for course credit.")
    if course_description:
        uni_courses = uni_courses.filter(course_description__icontains=course_description)

    # Sorting logic
    sort_order = request.GET.get('sort', 'asc')
    sort_by = request.GET.get('sort_by', 'course_code')  # Use a sort_by parameter
    if sort_order == 'desc':
        uni_courses = uni_courses.order_by(f'-{sort_by}')
    else:
        uni_courses = uni_courses.order_by(sort_by)

    # Create the context for the template
    context = {
        'courses': uni_courses,
    }

    # Render the course list page with the courses context
    return render(request, 'dashboard/courses-1.html', context)



def fte(request):
    faculties = Faculty.objects.all()

    # Start with an empty Q object
    query = Q()

    # Retrieve query parameters
    faculty_name = request.GET.get('faculty_name')
    year_of_joining = request.GET.get('year')
    semester = request.GET.get('semester')
    fte_value = request.GET.get('fte')

    # Dynamically build the query based on the presence of parameters
    if faculty_name:
        query &= Q(user__first_name__icontains=faculty_name) | Q(user__last_name__icontains=faculty_name)
    if year_of_joining:
        query &= Q(year_of_joining__icontains=year_of_joining)
    if semester:
        query &= Q(course_semester__icontains=semester)
    if fte_value:
        query &= Q(fte__icontains=fte_value)

    # Apply the constructed query to filter faculties
    faculties = faculties.filter(query)

    # Prepare a mapping for FTE divisor based on course type
    fte_divisor = {
        'CSCI_graduate': 186.23,
        'CSCI_undergrad': 406.24,
        'SENG_graduate': 90.17,
        'SENG_undergrad': 232.25,
        'DASC': 186.23,  # Assuming the same divisor for both graduate and undergraduate
    }

    # Calculate FTE for each faculty based on their courses
    for faculty in faculties:
        faculty_courses = faculty.course_set.all()  # Retrieve all courses associated with the faculty
        faculty.fte = sum(
            course.calculate_fte() for course in faculty_courses)  # Calculate FTE using the method in the Course model

    context = {
        'faculty': faculties,
    }

    return render(request, 'dashboard/fte.html', context)


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
