from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver


class RegularUser(models.Model):
    user_r = models.OneToOneField(User,on_delete=models.CASCADE)
    fb = models.URLField(blank=False)
    phone = models.CharField(max_length=11,default=0)
    city = models.CharField(max_length=20,blank=False)
    about_you = models.TextField(blank=True)
    photo = models.ImageField(upload_to="regular_user/")


    def __str__(self):
        return str(self.user_r)
    def get_Photo(self):
        return self.photo


class OrganizationUser(models.Model):
    user_o = models.OneToOneField(User,on_delete=models.CASCADE)
    o_name = models.CharField(max_length=30,blank=True)
    purpose = models.TextField(blank=False)
    web = models.URLField(blank=False)
    phone = models.CharField(max_length=11, default=0)
    city = models.CharField(max_length=20,blank=False)
    address = models.TextField(max_length=30,blank=False)
    photo = models.ImageField(upload_to="organization_user/", default='default.jpg')

    def __str__(self):
        return str(self.o_name)
    def title(self):
        return str(self.o_name)
class contactUs(models.Model):
    fullname = models.CharField(max_length=30,blank=False)
    email = models.EmailField(blank=False)
    phone = models.CharField(max_length=11,blank=False)
    company = models.CharField(max_length=30,blank=False)
    message = models.TextField(max_length=300,blank=False)
    post_on =models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.fullname}, {self.email}"


