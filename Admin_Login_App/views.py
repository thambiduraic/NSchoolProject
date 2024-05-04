import django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import  RegistrationForm, PartnersLogoForm, UpdataCourseForm
from .models import AdminLogin, courses, Testimonial
from .utils.validation import validate_course_data
from django.contrib import messages

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

# ------------------------------------------------------------------------------

def course_page_view(request):
    return render(request, 'Admin_Login_App/course_page.html')

def navbar_save_view(request):
    return render(request, 'Admin_Login_App/navbar_save_course.html')

# courses view
def courses_view(request):
    data = courses.objects.all()
    if request.method == 'POST':
        Title = request.POST.get('Title')
        Description = request.POST.get('Description')
        Technologies = request.POST.get('Technologies')
        Images = request.FILES.get('Images')
        status = request.POST.get('status')

        course_details = courses(
            Title=Title,
            Description=Description,
            Technologies=Technologies,
            Images=Images,
            status=status,
        )

        course_details.save()
        

        return redirect('courses')

    return render(request, 'Admin_Login_App/courses.html', {'datas': data})   

# courses update
def update_course(request, id):
    obj = courses.objects.get(id=id)
    if request.method == 'POST':
        form = UpdataCourseForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            return redirect('/courses')       
    return render(request, 'Admin_Login_App/course_update.html', {'form': obj}) 

# delete courses
def delete_course(request, id):
    obj = courses.objects.get(id=id)    
    obj.delete()
    return redirect('/courses')

# ----------------------------------------------------------

# Partners view

def partners_view(request):
    return render(request, 'Admin_Login_App/placement_partners.html')

# partners logo

def partners_logo_view(request):
    if request.method == 'POST':
        form = PartnersLogoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'success')
            return redirect('partners_list')
            # Get the current instance object to display in the template
            # img_obj = form.instance
            # return render(request, 'Admin_Login_App/partners_list.html')
        else:
            print(form.errors)
    else:
        form = PartnersLogoForm()
        return render(request, 'Admin_Login_App/partners_logo_form.html', {'form': form})

# ----------------------------------------------------------------------------------------------------

# testimonial_view

def testimonial_view(request):
    return render(request, 'Admin_Login_App/testimonial.html')


# testimonial_form_view

def testimonial_form_view(request):
    if request.method == 'POST':
        print("hi")
        try:
            student_name = request.POST.get('student_name')
            testimonial = request.POST.get('testimonial')
            course = request.POST.get('course')
            date = request.POST.get('date')
            picture = request.FILES.get('picture')
            
            testimonial_data = Testimonial(
                student_name=student_name,
                testimonial=testimonial,
                course=course,
                date=date,
                picture=picture,
            )
            testimonial_data.save()

            # Get existing testimonials to display in the form
            testimonials = Testimonial.objects.all()

            # Redirect to the 'testimonial_list' page after successful form submission
            return render(request, 'Admin_Login_App/testimonial_list.html', {'testimonials': testimonials})
        except Exception as e:
            print("Error saving testimonial:", e)
            # You can log the error or handle it in other ways, such as displaying an error message to the user

    # If it's not a POST request, render the form page
    return render(request, 'Admin_Login_App/testimonial_form.html')

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