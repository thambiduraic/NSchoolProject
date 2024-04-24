import django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import  RegistrationForm
from .models import AdminLogin, courses
from .utils.validation import validate_course_data

# Create your views here.

# decorator operation
def decorator(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('login')
    return inner

@decorator
def home(request):
    return render(request, 'Admin_Login_App/home.html')

def user_home(request):
    return render(request, 'Admin_Login_App/User_Login.html')

# dashboard view
def dashboard_view(request):
    return render(request, 'Admin_Login_App/Admin_Body.html')

# courses view
def courses_view(request):
    
    if request.method == 'POST':
        Title = request.POST.get('Title')
        Description = request.POST.get('Description')
        Technologies = request.POST.get('Technologies')
        Images = request.POST.get('Images')
        status = request.POST.get('status')

        course_data = {'Title':Title, 'Description':Description, 'Technologies':Technologies, 'Images':Images, 'status':status}

        validation_error = validate_course_data(course_data)

        if not validation_error:

            course_details = courses(
                title=form.cleaned_data['Title'],
                description=form.cleaned_data['Description'],
                technologies=form.cleaned_data['Technologies'],
                images=form.cleaned_data['Images'],
                status=form.cleaned_data['status']
            )
            course_details.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'Admin_Login_App/courses.html')

# admin login view    

def admin_login_view(request):
    error_message = None  # Initialize error variable

    if request.method == 'POST':
        # Get the input data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            
            # Redirect based on user role
            if user.is_admin:
                return redirect('dashboard')  # Redirect to admin home page
            else:
                return redirect('admin_login')  # Redirect to user home page
        else:
            # Authentication failed
            error_message = 'Invalid username or password'
    
    # Render the login page with the error message if any
    return render(request, 'Admin_Login_App/AdminLogin.html', {'error': error_message})


# register view

def register_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'Admin_Login_App/register.html', {'form' : form})


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(
            username = username,
            password = password,
        )

        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('login')
            else:
                return redirect('user_home')
            
    
    return render(request, 'Admin_Login_App/AdminLogin.html')

# Logout operation

def logout(request):
    if request.user.is_authenticated:
        django.contrib.auth.logout(request)
        return redirect('admin_login')


def user_logout(request):
    if request.user.is_authenticated:
        django.contrib.auth.logout(request)
        return redirect('home')