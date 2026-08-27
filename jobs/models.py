from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class jobs(models.Model):
    recruiter = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posted_jobs")
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    skills_required = models.TextField(blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Application(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    job = models.ForeignKey(jobs,on_delete=models.CASCADE)
    applied_at =models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,default='Pending')
    feedback = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"