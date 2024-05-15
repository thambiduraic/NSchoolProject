from rest_framework import serializers
from Admin_Login_App.models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses
        fields = ['Title', 'Description', 'Technologies', 'Images', 'status']

class PlacementPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = partners_logo
        fields = ['name', 'logo']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['student_name', 'picture', 'course', 'date', 'testimonial']

class PlacementStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementStories
        fields = ['student_name', 'course', 'testimonial_video', 'date']

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['images', 'title', 'description', 'course']

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Careers
        fields = ['Logo', 'Job_Heading', 'Location', 'Experience', 'No_Of_Openings', 'Salary', 'Status', 'Job_Type', 'Qualification', 'Job_Description', 'Skills_Required']