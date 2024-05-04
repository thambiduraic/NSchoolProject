from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AdminLogin, partners_logo, courses

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

class UpdataCourseForm(forms.ModelForm):
    class Meta:
        model = courses
        fields = ['Title', 'Technologies', 'status']