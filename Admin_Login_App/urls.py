from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.home, name='home'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('courses', views.courses_view, name='courses'),
    path('course_page', views.course_page_view, name='course_page'),
    path('update_course/<int:id>', views.update_course, name='update_course'),
    path('delete_course/<id>', views.delete_course),
    path('navbar_save_course', views.navbar_save_view, name='navbar_save_course'),
    path('partners_logo', views.partners_logo_view, name='partners_logo'),
    path('partners', views.partners_view, name='partners'),
    path('testimonial', views.testimonial_view, name='testimonial'),
    path('testimonial_form', views.testimonial_form_view, name='testimonial_form'),
    path('placement_stories', views.Placement_Stories_view, name='placement_stories'),
    path('stories_form', views.stories_form, name='stories_form'),
    path('faq', views.faq, name='faq'),
    path('faq_add_form', views.faq_add_form, name='faq_add_form'),
    path('blog', views.blog_view, name='blog'),
    path('blog_add_form', views.blog_form, name='blog_add_form'),
    path('careers', views.Careers_view, name='careers'),
    path('careers_form', views.Careers_form_view, name='careers_form'),
    path('user_home', views.user_home, name='user_home'),
    path('login', views.login_view, name='login'),
    path('admin_login', views.admin_login_view, name='admin_login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('user_logout', views.user_logout, name='user_logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)