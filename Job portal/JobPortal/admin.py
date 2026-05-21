from django.contrib import admin
from JobPortal.models import *
# Register your models here.

admin.site.register([
    User,
    RecruiterProfileModel,
    JobSeerkerProfileModel,
    JobPostModel,
    ApplyJobModel,
    CategoryModel,
])
