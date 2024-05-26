from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ckeditor.widgets import CKEditorWidget  # Import CKEditorWidget
from .models import *

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = AdminLogin
        fields = ('username', 'email', 'ph_no', 'password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

class PartnersLogoForm(forms.ModelForm):
    class Meta:
        model = partners_logo
        fields = ['name', 'logo']

class UpdataCourseForm(forms.Form):
    Title = forms.CharField(max_length=100)
    Description = forms.CharField(widget=forms.Textarea)
    Technologies = forms.CharField(max_length=150)
    Images = forms.ImageField()
    status = forms.BooleanField()

class FaqForm(forms.ModelForm):  # Change to ModelForm
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
        widgets = {
            'answer': CKEditorWidget()  # Use CKEditorWidget for 'answer' field
        }
