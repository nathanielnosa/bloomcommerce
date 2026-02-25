from django.db import models
from django.contrib.auth.models import User

GENDER = (
    ('M','male'),
    ('F','Female'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=225)
    gender = models.CharField(max_length=6,choices=GENDER)
    phone = models.CharField(max_length=15)
    profile_pix = models.ImageField(upload_to='profile',default="me.jpg",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname
    