from django.contrib import admin
from .models import AdminLogin, courses, FAQ

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    # Specify the fields to be displayed in the admin interface
    list_display = ['Title', 'Description', 'Technologies', 'Images', 'status']

# Register the CourseAdmin with the courses model
admin.site.register(courses, CourseAdmin)

# Register the AdminLogin and FAQ models
admin.site.register(AdminLogin)
admin.site.register(FAQ)



