import django
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.contrib.auth import login, authenticate, logout
from .forms import *
from .models import *
# from .utils.validation import validate_course_data
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser, MultiPartParser
from django.http import JsonResponse
from Admin_Login_App.serializers import *
from rest_framework.decorators import parser_classes, api_view

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
            print(images)
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
    course = courses.objects.get(id=id)

    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('Title')
        description = request.POST.get('Description')
        technologies = request.POST.get('Technologies')
        status = request.POST.get('status')
        images = request.FILES.get('Images')

        print(title)

        # Update the attributes of the existing course object
        course.Title = title
        course.Description = description
        course.Technologies = technologies
        course.status = status

        # Check if a new image is provided
        if images:
            course.Images = images

        # Save the updated course object
        course.save()

        return redirect('/courses')

    else:
        # Render form with existing course data
        return render(request, 'Admin_Login_App/course_update.html', {'datas': course}) 

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

# update partners
def update_partners(request, id):
    data = partners_logo.objects.get(id=id)
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        logo = request.FILES.get('logo')

        # Update the object with new data
        data.name = name
        if logo:  # Check if a file was uploaded
            data.logo = logo

        # Save the updated object
        data.save()
        return redirect('/partners')
    return render(request, 'Admin_Login_App/update_partners.html', {'datas': data})


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

# update testimonial

def update_testimonial(request, id):
    data = Testimonial.objects.get(id=id)
    if request.method == 'POST':
        try:
            student_name = request.POST.get('student_name')
            testimonial_text = request.POST.get('testimonial')
            course = request.POST.get('course')
            date = request.POST.get('date')
            picture = request.FILES.get('picture')
            
            # Assign values to data object's fields
            data.student_name = student_name
            data.testimonial = testimonial_text
            data.course = course
            data.date = date

            # Update picture if provided
            if picture:
                data.picture = picture
            
            data.save()
            return redirect('/testimonial')
        except Exception as e:
            print("Error saving testimonial:", e)
    return render(request, 'Admin_Login_App/testimonial_update.html', {'datas': data})


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


# stories update

def update_stories(request, id):
    data = PlacementStories.objects.get(id=id)
    if request.method == 'POST':
        try:
            student_name = request.POST.get('student_name')
            course = request.POST.get('course')
            testimonial_video = request.FILES.get('testimonial_video')
            date = request.POST.get('date')
            
            
            data.student_name = student_name
            data.course = course
            data.testimonial_video = testimonial_video
            data.date = date
            
            data.save()

            return redirect('placement_stories')
        
        except Exception as e:
            print("Error saving testimonial:", e)
    return render(request, 'Admin_Login_App/stories_update.html', {'datas': data})

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

# faq form update

def faq_form_update(request, id):
    faq = get_object_or_404(FAQ, id=id)

    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        if question and answer:
            faq.question = question
            faq.answer = answer
            try:
                faq.save()
                return redirect('faq')
            except Exception as e:
                # Log the error
                print(f"Error occurred while updating FAQ: {e}")
                return HttpResponseServerError("An error occurred while updating FAQ. Please try again later.")
        else:
            # Handle missing question or answer
            return HttpResponseBadRequest("Question and answer are required fields.")
    else:
        # Handle GET request to render update form
        return render(request, 'Admin_Login_App/faq_update_form.html', {'data': faq})



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

# update blog

def update_blog(request, id):
    data = Blog.objects.get(id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course = request.POST.get('course')
        images = request.FILES.get('images')

        data.title=title
        data.description=description
        data.course=course

        if images:
            data.images=images
        
        data.save()
        return redirect('blog')
    return render(request, 'Admin_Login_App/update_blog.html', {'datas': data})

# carrers view
@decorator_admin
def Careers_view(request):
    data = Careers.objects.all().order_by('Job_Heading')
    if request.method == 'POST':
        try:
            Logo = request.FILES.get('Logo')
            Job_Heading = request.POST.get('Job_Heading')
            Location = request.POST.get('Location')
            Experience = request.POST.get('Experience')
            No_Of_Openings = request.POST.get('No_Of_Openings')
            Salary = request.POST.get('Salary')
            Status = request.POST.get('Status')
            Job_Type = request.POST.get('Job_Type')
            Qualification = request.POST.get('Qualification')
            Job_Description = request.POST.get('Job_Description')
            Skills_Required = request.POST.get('Skills_Required')
            
            careers_data = Careers(
                Logo = Logo,
                Job_Heading = Job_Heading,
                Location = Location,
                Experience = Experience,
                No_Of_Openings = No_Of_Openings,
                Salary = Salary,
                Status = Status,
                Job_Type = Job_Type,
                Qualification = Qualification,
                Job_Description = Job_Description,
                Skills_Required = Skills_Required,
            )
            careers_data.save()

            return redirect('careers')
        
        except Exception as e:
            print("Error saving careers:", e)
    
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
    return render(request, 'Admin_Login_App/Careers.html', {'page_obj': page_obj})
    # return render(request, 'Admin_Login_App/Careers.html')

def Careers_form_view(request):
    return render(request, 'Admin_Login_App/careers_form.html')

# update career

def update_career(request, id):
    data = Careers.objects.get(id=id)
    if request.method == 'POST':
        try:
            Logo = request.FILES.get('Logo')
            Job_Heading = request.POST.get('Job_Heading')
            Location = request.POST.get('Location')
            Experience = request.POST.get('Experience')
            No_Of_Openings = request.POST.get('No_Of_Openings')
            Salary = request.POST.get('Salary')
            Status = request.POST.get('Status')
            Job_Type = request.POST.get('Job_Type')
            Qualification = request.POST.get('Qualification')
            Job_Description = request.POST.get('Job_Description')
            Skills_Required = request.POST.get('Skills_Required')
            
            if Logo:
                data.Logo = Logo
            
            data.Job_Heading = Job_Heading
            data.Location = Location
            data.Experience = Experience
            data.No_Of_Openings = No_Of_Openings
            data.Salary = Salary
            data.Status = Status
            data.Job_Type = Job_Type
            data.Qualification = Qualification
            data.Job_Description = Job_Description
            data.Skills_Required = Skills_Required
            
            data.save()

            return redirect('careers')
        
        except Exception as e:
            print("Error saving careers:", e)
    return render(request, 'Admin_Login_App/update_careers.html', {'datas': data})

# report view
def report_view(request):
    if request.method == 'POST':
        selected_value = int(request.POST.get('one'))
        if selected_value == 1:
            data = courses.objects.all()
        elif selected_value == 2:
            data = partners_logo.objects.all()
        elif selected_value == 3:
            data = Testimonial.objects.all()  
        elif selected_value == 4:
            data = PlacementStories.objects.all()  
        elif selected_value == 5:
            data = FAQ.objects.all()
        elif selected_value == 6:
            data = Blog.objects.all()
        elif selected_value == 7:
            data = Careers.objects.all()

        paginator = Paginator(data, 5)

        page_number = request.GET.get("page")
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(request, 'Admin_Login_App/Reports.html', {'page_obj': page_obj})

    return render(request, 'Admin_Login_App/Reports.html')

# admin login view    

def admin_login_view(request):
    error_message = None  # Initialize error variable
    username = ""  # Initialize username variable

    if request.method == 'POST':
        # Get the input data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username or password is empty
        if username and not password or not username and password:
            error_message = 'No match for Username and/or Password'

        elif not username or not password:
            error_message = 'Username and Password are required.'
        
        else:
            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                # Check if the user account is active
                if user.is_active:
                    # Log in the user
                    login(request, user)
                    
                    # Redirect based on user role
                    if user.is_admin:
                        return redirect('dashboard')  # Redirect to admin home page
                    else:
                        return redirect('admin_login')  # Redirect to user home page
                else:
                    # User account is inactive
                    error_message = 'Your account is inactive. Please contact support for assistance.'
            else:
                # Authentication failed
                error_message = 'Invalid Username or Password'

    # Render the login page with the error message if any
    return render(request, 'Admin_Login_App/AdminLogin.html', {'error': error_message, 'username':username})


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


# course api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def courseApi(request, id=0):
    
    if request.method == 'POST':
        course_serializer = CourseSerializer(data = request.data)
        if course_serializer.is_valid():
            course_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        course = courses.objects.all()
        course_serializer = CourseSerializer(course, many=True)
        return JsonResponse(course_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        course_data = request.data
        course = courses.objects.get(id=id)
        course_serializer = CourseSerializer(course, data=course_data)
        if course_serializer.is_valid():
            course_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            account = courses.objects.get(id=id)
            account.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# Placement Partners Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def placementPartnersApi(request, id=0):
    
    if request.method == 'POST':
        placement_partners_serializer = PlacementPartnersSerializer(data = request.data)
        if placement_partners_serializer.is_valid():
            placement_partners_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        partners = partners_logo.objects.all()
        placement_partners_serializer = PlacementPartnersSerializer(partners, many=True)
        return JsonResponse(placement_partners_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        partners_data = request.data
        partners = partners_logo.objects.get(id=id)
        placement_partners_serializer = PlacementPartnersSerializer(partners, data=partners_data)
        if placement_partners_serializer.is_valid():
            placement_partners_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            partners = partners_logo.objects.get(id=id)
            partners.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)


# Testimonial Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def testimonialApi(request, id=0):
    
    if request.method == 'POST':
        testimonial_serializer = TestimonialSerializer(data = request.data)
        if testimonial_serializer.is_valid():
            testimonial_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        testimonial = Testimonial.objects.all()
        testimonial_serializer = TestimonialSerializer(testimonial, many=True)
        return JsonResponse(testimonial_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        testimonial_data = request.data
        testimonial = Testimonial.objects.get(id=id)
        testimonial_serializer = TestimonialSerializer(testimonial, data=testimonial_data)
        if testimonial_serializer.is_valid():
            testimonial_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            testimonial = Testimonial.objects.get(id=id)
            testimonial.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# PlacementStories Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def placementStoriesApi(request, id=0):
    
    if request.method == 'POST':
        placement_stories_serializer = PlacementStoriesSerializer(data = request.data)
        if placement_stories_serializer.is_valid():
            placement_stories_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        placement_stories = PlacementStories.objects.all()
        placement_stories_serializer = PlacementStoriesSerializer(placement_stories, many=True)
        return JsonResponse(placement_stories_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        placement_stories_data = request.data
        placement_stories = PlacementStories.objects.get(id=id)
        placement_stories_serializer = PlacementStoriesSerializer(placement_stories, data=placement_stories_data)
        if placement_stories_serializer.is_valid():
            placement_stories_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            placement_stories = PlacementStories.objects.get(id=id)
            placement_stories.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# FAQ Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def FaqApi(request, id=0):
    
    if request.method == 'POST':
        faq_serializer = FaqSerializer(data = request.data)
        if faq_serializer.is_valid():
            faq_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        faq = FAQ.objects.all()
        faq_serializer = FaqSerializer(faq, many=True)
        return JsonResponse(faq_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        faq_data = request.data
        faq = FAQ.objects.get(id=id)
        faq_serializer = FaqSerializer(faq, data=faq_data)
        if faq_serializer.is_valid():
            faq_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            faq_serializer = FAQ.objects.get(id=id)
            faq_serializer.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# Blog Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def BlogApi(request, id=0):
    
    if request.method == 'POST':
        blog_serializer = BlogSerializer(data = request.data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        blog = Blog.objects.all()
        blog_serializer = BlogSerializer(blog, many=True)
        return JsonResponse(blog_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        blog_data = request.data
        blog = Blog.objects.get(id=id)
        blog_serializer = BlogSerializer(blog, data=blog_data)
        if blog_serializer.is_valid():
            blog_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            blog_serializer = Blog.objects.get(id=id)
            blog_serializer.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)

# Careers Api

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def CareerApi(request, id=0):
    
    if request.method == 'POST':
        career_serializer = CareerSerializer(data = request.data)
        if career_serializer.is_valid():
            career_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    
    elif request.method == 'GET':
        career = Careers.objects.all()
        career_serializer = CareerSerializer(career, many=True)
        return JsonResponse(career_serializer.data, safe=False)
    
    elif request.method == 'PUT':
        career_data = request.data
        career = Careers.objects.get(id=id)
        career_serializer = CareerSerializer(career, data=career_data)
        if career_serializer.is_valid():
            career_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    
    elif request.method == 'DELETE':
        try:
            career_serializer = Careers.objects.get(id=id)
            career_serializer.delete()
            return JsonResponse("Deleted Successfully", safe=False)
        except courses.DoesNotExist:
            return JsonResponse("Account does not exist", status=404, safe=False)