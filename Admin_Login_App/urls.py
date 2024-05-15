from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.home, name='home'),

    # api urls

    # course api
    path('course_api', views.courseApi, name='course_api'),
    path('update_course_api/<int:id>', views.courseApi, name='update_course_api'),
    path('delete_course_api/<int:id>', views.courseApi, name='delete_course_api'),

    # placement partners api
    path('partners_api', views.placementPartnersApi, name='partners_api'),
    path('update_partners_api/<int:id>', views.placementPartnersApi, name='update_partners_api'),
    path('delete_partners_api/<int:id>', views.placementPartnersApi, name='delete_partners_api'),

    # testimonial api
    path('testimonial_api', views.testimonialApi, name='testimonial_api'),
    path('update_testimonial_api/<int:id>', views.testimonialApi, name='update_testimonial_api'),
    path('delete_testimonial_api/<int:id>', views.testimonialApi, name='delete_testimonial_api'),

    # placement stories api
    path('placement_stories_api', views.placementStoriesApi, name='placement_stories_api'),
    path('update_placement_stories_api/<int:id>', views.placementStoriesApi, name='update_placement_stories_api'),
    path('delete_placement_stories_api/<int:id>', views.placementStoriesApi, name='delete_placement_stories_api'),

    # faq api
    path('faq_api', views.FaqApi, name='faq_api'),
    path('update_faq_api/<int:id>', views.FaqApi, name='update_faq_api'),
    path('delete_faq_api/<int:id>', views.FaqApi, name='delete_faq_api'),

    # blog api
    path('blog_api', views.BlogApi, name='blog_api'),
    path('update_blog_api/<int:id>', views.BlogApi, name='update_blog_api'),
    path('delete_blog_api/<int:id>', views.BlogApi, name='delete_blog_api'),

    # career api
    path('career_api', views.CareerApi, name='career_api'),
    path('update_career_api/<int:id>', views.CareerApi, name='update_career_api'),
    path('delete_career_api/<int:id>', views.CareerApi, name='delete_career_api'),

    path('dashboard', views.dashboard_view, name='dashboard'),
    path('courses', views.courses_view, name='courses'),
    path('course_page', views.course_page_view, name='course_page'),
    path('update_course/<int:id>', views.update_course, name='update_course'),
    path('delete_course/<id>', views.delete_course),
    path('navbar_save_course', views.navbar_save_view, name='navbar_save_course'),
    path('partners_logo', views.partners_logo_view, name='partners_logo'),
    path('partners', views.partners_view, name='partners'),
    path('update_partners/<int:id>', views.update_partners, name='update_partners'),
    path('testimonial', views.testimonial_view, name='testimonial'),
    path('testimonial_form', views.testimonial_form_view, name='testimonial_form'),
    path('update_testimonial/<int:id>', views.update_testimonial, name='update_testimonial'),
    path('placement_stories', views.Placement_Stories_view, name='placement_stories'),
    path('update_stories/<int:id>', views.update_stories, name='update_stories'),
    path('stories_form', views.stories_form, name='stories_form'),
    path('faq', views.faq, name='faq'),
    path('faq_form_update/<int:id>/', views.faq_form_update, name='faq_form_update'),
    path('faq_add_form', views.faq_add_form, name='faq_add_form'),
    path('blog', views.blog_view, name='blog'),
    path('blog_add_form', views.blog_form, name='blog_add_form'),
    path('update_blog/<int:id>/', views.update_blog, name='update_blog'),
    path('careers', views.Careers_view, name='careers'),
    path('careers_form', views.Careers_form_view, name='careers_form'),
    path('update_careers/<int:id>/', views.update_blog, name='update_careers'),
    path('user_home', views.user_home, name='user_home'),
    path('login', views.login_view, name='login'),
    path('admin_login', views.admin_login_view, name='admin_login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('report', views.report_view, name='report'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)