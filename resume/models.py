from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Resume(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resume/')
    score = models.IntegerField(default=0)
    skills = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)




def __str__(self):
    return self.user.username