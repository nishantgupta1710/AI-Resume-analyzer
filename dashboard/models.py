from django.db import models
from django.contrib.auth.models import User

class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=150)

    hr_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    location = models.CharField(max_length=100)

    website = models.URLField(blank=True)

    about_company = models.TextField(blank=True)

    role = models.CharField(max_length=20,default="Recruiter")

    def _str_(self):
        return self.company_name
