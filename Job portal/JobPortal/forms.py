from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from JobPortal.models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','display_name','email','user_type','password1','password2']


class LoginForm(AuthenticationForm):
    pass

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfileModel
        fields = '__all__'
        exclude = ['recruiter']

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeerkerProfileModel
        fields = '__all__'
        exclude = ['jobseeker']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPostModel
        fields = '__all__'
        exclude = ['posted_by']
        widgets = {
            'deadline' : forms.DateInput(
                attrs={
                    'type':'date'
                }
            )
        }
class ApplyJobForm(forms.ModelForm):
  class Meta:
    model = ApplyJobModel
    fields = ['resume']