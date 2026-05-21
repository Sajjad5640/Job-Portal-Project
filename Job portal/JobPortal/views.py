from django.shortcuts import render,redirect
from JobPortal.models import *
from JobPortal.forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_page(request):

    if request.method == "POST":
        form_data = RegistrationForm(request.POST)

        if form_data.is_valid():
            form_data.save()
            messages.success(request, "User Creation Successfully!!")
            return redirect('login_page')

    else:
        form_data = RegistrationForm()

    context = {
        'form_data': form_data,
        'title': 'Register Page',
        'form_title': 'User Registration Form',
        'form_btn': 'Register',
    }

    return render(request, 'master/base-form.html', context)

def login_page(request):
    if request.method == "POST":
        form_data = LoginForm(request,request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            if user:
                login(request,user)
                messages.success(request,"User Login Successfully")
                return redirect('dashboard_page')
        messages.error(request,"Invalid Credintial")

    form_data = LoginForm()
    context = {
        'form_data':form_data,
        'title' : 'Login Page',
        'form_title': 'Login Form',
        'form_btn':'Login',
    }
    return render (request, 'master/base-form.html', context)

@login_required
def dashboard_page(request):
    try:
        seeker_data = request.user.jobseeker_profile
    except:
        messages.error(request, 'Please, Update your profile first.')
        return redirect('update_profile')
    if request.user.user_type =='Jobseekers':
        seeker_skill = request.user.jobseeker_profile.skills_set
        job_data = JobPostModel.objects.none()
        for skill in seeker_skill.split(','):
            cleaned_skill = skill.strip()
            job_data |= JobPostModel.objects.filter(skills_set__icontains = cleaned_skill)

    context = {
        'job_data': job_data
    }
    return render (request,'dashboard_page.html',context)
@login_required
def logout_page(request):
    logout(request)
    return redirect("login_page")
@login_required
def profile_page(request):

    return render (request,'profile.html')
@login_required
def update_profile(request):

    current_user = request.user

    if current_user.user_type == 'Recruiters':
        try:
            profile_data = RecruiterProfileModel.objects.get(recruiter = current_user)
        except:
            profile_data = None

        if request.method == "POST":
            form_data = RecruiterProfileForm(request.POST,request.FILES, instance=profile_data)
            if form_data.is_valid():
                data = form_data.save(commit= False)
                data.recruiter = current_user
                data.save()
                messages.success (request,'Profile Update SUccessfully!!')
                return redirect('profile_page')

        form_data = RecruiterProfileForm(instance=profile_data)
    else:
        try:
            profile_data = JobSeerkerProfileModel.objects.get(jobseeker = current_user)
        except:
            profile_data = None
        if request.method == "POST":
            form_data = JobSeekerProfileForm(request.POST,request.FILES, instance=profile_data)
            if form_data.is_valid():
                data = form_data.save(commit= False)
                data.jobseeker = current_user
                data.save()
                messages.success (request,'Profile Update SUccessfully!!')
                return redirect('profile_page')
        form_data = JobSeekerProfileForm(instance=profile_data)

    context = {
        'form_data':form_data,
        'title' : 'Update Profile',
        'form_title': 'Update Your Profile',
        'form_btn':'Update',
    }
    return render (request,'master/base-form.html',context)

def browse_job_view(request):
    current_user = request.user
    search_query = request.GET.get('search_query')
    print(current_user)
    job_data = JobPostModel.objects.all()

    if current_user.is_authenticated:
        if current_user.user_type == 'Recruiters':
            try:
                job_data = JobPostModel.objects.filter(posted_by = current_user.recruiter_profile)
            except:
                messages.error(request, 'Please, Update your profile first.')
                return redirect('update_profile')

    if search_query:
        # job_data = JobPostModel.objects.filter(title =search_query)
        # job_data = JobPostModel.objects.filter(title__icontains = search_query)
        job_data = JobPostModel.objects.filter(
            Q(title__icontains = search_query) |
            Q(category__name__icontains = search_query) |
            Q(posted_by__company_name__icontains = search_query)

        )
    context = {
        'job_data': job_data
    }
    return render(request,'browse-jobs.html', context)
@login_required
def post_job_view(request):
    try:
        recruiter_data =  request.user.recruiter_profile
    except:
        messages.error(request,"Update your profile")
        return redirect('update_profile')
    if request.method == "POST":
        form_data = JobPostForm(request.POST,request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit= False)
            data.posted_by = recruiter_data
            data.save()
            messages.success (request,'Job Posted SUccessfully!!')
            return redirect('browse_job_view')

    form_data = JobPostForm()
    context = {
        'form_data':form_data,
        'title' : 'Post Job page',
        'form_title': 'Post Job Info Form',
        'form_btn':'Post',
    }
    return render(request,'master/base-form.html',context)

@login_required
def update_job_view(request, id):
    try:
        recruiter_data = request.user.recruiter_profile
        job = JobPostModel.objects.get(id = id)
    except:
        messages.error(request, 'Please, Update your profile first.')
        return redirect('update_profile')

    if request.method == 'POST':
        form_data = JobPostForm(request.POST, request.FILES, instance=job)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.posted_by = recruiter_data
            data.save()
            messages.success(request, 'Job Updated Successfully.')
            return redirect('browse_job_view')

    form_data = JobPostForm(instance=job)
    context = {
        'form_data': form_data,
        'title': 'Update Job Page',
        'form_title': 'Update Job Info Form',
        'form_btn': 'Update',
    }
    return render(request, 'master/base-form.html', context)
@login_required
def delete_job_view(request, id):
    try:
        JobPostModel.objects.get(id = id).delete()
        messages.error(request, 'Job Deleted successfully.')
        return redirect('browse_job_view')
    except:
        messages.error(request, 'Job Not Found.')
        return redirect('browse_job_view')

@login_required
def apply_job_view(request,id):
    try:
        seeker_profile = request.user.jobseeker_profile
        job = JobPostModel.objects.get(id=id)
    except:
        messages.error(request, 'Please, Update your profile first.')
        return redirect('update_profile')
    if request.method == "POST":
        form_data = ApplyJobForm(request.POST,request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.applied_by =seeker_profile
            data.applied_job = job
            data.save()
            return redirect('browse_job_view')

    form_data = ApplyJobForm()

    context = {
        'form_data': form_data,
        'title': 'Apply Job Page',
        'form_title': 'Apply Job Info Form',
        'form_btn': 'Apply',
    }
    return render(request, 'master/base-form.html', context)

def my_application (request):

    my_application = ApplyJobModel.objects.filter(applied_by = request.user.jobseeker_profile)


    context = {

        'application_list':my_application,
        'title': 'My application  Page',
        'form_title': 'Apply Job Info Form',
        'form_btn': 'Apply',
    }
    return render (request,'my-application.html',context)

def candidate_list_view(request,id):
    job_data = JobPostModel.objects.get(id = id)
    candidate_data = ApplyJobModel.objects.filter(applied_job = job_data)

    context = {
        'candidate_data':candidate_data,
        'job_data':job_data,
        'application_list':my_application,
        'title': 'Candidate List Page',
    }
    return render (request,'candidate-list.html',context)