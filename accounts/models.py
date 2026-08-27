from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CandidateProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=100)
    skills = models.TextField()
    role = models.CharField(max_length=20,default = 'Candidate')


    def __str__(self):
        return self.user.username