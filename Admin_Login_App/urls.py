from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home, name='home'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('courses', views.courses_view, name='courses'),
    path('user_home', views.user_home, name='user_home'),
    path('login', views.login_view, name='login'),
    path('admin_login', views.admin_login_view, name='admin_login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout, name='logout'),
    path('user_logout', views.user_logout, name='user_logout'),
]