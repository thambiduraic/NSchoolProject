import django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import  RegistrationForm, PartnersLogoForm, UpdataCourseForm
from .models import AdminLogin, courses, Testimonial, FAQ, Blog, partners_logo, PlacementStories
# from .utils.validation import validate_course_data
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

# decorator operation
def decorator(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('login')
    return inner

# decorator for admin
def decorator_admin(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return redirect('admin_login')
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
@decorator_admin
def courses_view(request):
    # data = courses.objects.all()
    data = courses.objects.all().order_by('Title')
    if request.method == 'POST':
        try:
            title = request.POST.get('Title')
            description = request.POST.get('Description')
            technologies = request.POST.get('Technologies')
            images = request.FILES.get('images')
            status = request.POST.get('status')
            
            courses_data = courses(
                Title = title,
                Description = description,
                Technologies = technologies,
                Images = images,
                status = status,
            )
            courses_data.save()

            return redirect('courses')
        
        except Exception as e:
            print("Error saving courses:", e)
    
    paginator = Paginator(data, 5)  # Show 5 contacts per page.

    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'Admin_Login_App/courses.html', {'page_obj': page_obj})

    # return render(request, 'Admin_Login_App/courses.html', {'datas': data, "page_obj": page_obj})  

# courses update
def update_course(request, id):
    obj = courses.objects.get(id=id)
    print(obj)
    if request.method == 'POST':
        try:
            title = request.POST.get('Title')
            description = request.POST.get('Description')
            technologies = request.POST.get('Technologies')
            images = request.FILES.get('images')
            status = request.POST.get('status')

            if title and description and technologies and images and status:
                courses_data = courses(
                Title = title,
                Description = description,
                Technologies = technologies,
                Images = images,
                status = status,
            )
            courses_data.save()
            return redirect('courses')
        
        except Exception as e:
            print("Error saving courses:", e)
    return render(request, 'Admin_Login_App/course_update.html', {'datas': obj}) 

# delete courses
def delete_course(request, id):
    obj = courses.objects.get(id=id)    
    obj.delete()
    return redirect('/courses')

# ----------------------------------------------------------

# Partners view
@decorator_admin
def partners_view(request):
    form = partners_logo.objects.all().order_by('name')
    if request.method == 'POST':
        try:
            name = request.POST.get('student_name')
            images = request.POST.FILES.get('picture')
            
            partners_data = Testimonial(
                name=name,
                images=images,
            )
            partners_data.save()

            # Redirect to the 'testimonial_list' page after successful form submission
            return redirect('partners')
        except Exception as e:
            print("Error saving partners:", e)

    paginator = Paginator(form, 5)  # Show 5 contacts per page.

    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'Admin_Login_App/placement_partners.html', {'page_obj': page_obj})
    # return render(request, 'Admin_Login_App/placement_partners.html', {'form': form})

# partners logo

def partners_logo_view(request):
    return render(request, 'Admin_Login_App/partners_logo_form.html')

# ----------------------------------------------------------------------------------------------------

# testimonial_view
@decorator_admin
def testimonial_view(request):
    # testimonials = Testimonial.objects.all()
    testimonials = Testimonial.objects.all().order_by('student_name')
    if request.method == 'POST':
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

            # Redirect to the 'testimonial_list' page after successful form submission
            return redirect('testimonial')
        except Exception as e:
            print("Error saving testimonial:", e)

    paginator = Paginator(testimonials, 5)  # Show 5 contacts per page.

    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'Admin_Login_App/testimonial.html', {'page_obj': page_obj})
    # return render(request, 'Admin_Login_App/testimonial.html', {'testimonials': testimonials})


# testimonial_form_view

def testimonial_form_view(request):
    return render(request, 'Admin_Login_App/testimonial_form.html')

# Placement Stories
@decorator_admin
def Placement_Stories_view(request):
    form = PlacementStories.objects.all().order_by('student_name')
    if request.method == 'POST':
        try:
            student_name = request.POST.get('student_name')
            course = request.POST.get('course')
            testimonial_video = request.FILES.get('testimonial_video')
            date = request.POST.get('date')
            
            stories_data = PlacementStories(
                student_name=student_name,
                course=course,
                testimonial_video=testimonial_video,
                date=date,
            )
            stories_data.save()

            # Redirect to the 'testimonial_list' page after successful form submission
            return redirect('placement_stories')
        except Exception as e:
            print("Error saving testimonial:", e)
    
    paginator = Paginator(form, 5)  # Show 5 contacts per page.

    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'Admin_Login_App/placement_stories.html', {'page_obj': page_obj})

    # return render(request, 'Admin_Login_App/placement_stories.html', {'form':form})

# placement stories form

def stories_form(request):
    return render(request, 'Admin_Login_App/stories_form.html')

# FAQ
@decorator_admin
def faq(request):
    data = FAQ.objects.all().order_by('question')
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        # Check if both question and answer are provided
        if question and answer:
            faq_data = FAQ(question=question, answer=answer)
            faq_data.save()
            return redirect('faq')
        else:
            # Handle the case where either question or answer is missing
            error_message = "Both question and answer are required."
            return render(request, 'Admin_Login_App/faq_add_form.html', {'error_message': error_message})
    
    paginator = Paginator(data, 5)  # Show 5 contacts per page.

    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'Admin_Login_App/Faq.html', {'page_obj': page_obj})

    # return render(request, 'Admin_Login_App/Faq.html', {'datas': data})


def faq_add_form(request):
    return render(request, 'Admin_Login_App/faq_add_form.html')


# blog_view
@decorator_admin
def blog_view(request):
    data = Blog.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course = request.POST.get('course')
        images = request.FILES.get('images')

        if title and description and course:
            blog_data = Blog(title=title, description=description, course=course, images=images)
            blog_data.save()
            return redirect('blog')

    paginator = Paginator(data, 5)  # Show 5 contacts per page.

    page_number = request.GET.get("page")
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'Admin_Login_App/blog.html', {'page_obj': page_obj})
    # return render(request, 'Admin_Login_App/blog.html', {'datas': data})

def blog_form(request):
    return render(request, 'Admin_Login_App/blog_add_form.html')

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

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('admin_login')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')
    