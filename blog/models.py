from django.db import models
from django_cryptography.fields import encrypt
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .settings import MEDIA_ROOT

class User(AbstractUser):
	last_login = encrypt(models.DateField(null=True))
	is_superuser = encrypt(models.BooleanField(default=False))
	email = encrypt(models.CharField('',max_length=254))
	
	hashed_email = models.CharField('',max_length=256, default=None)
	
	is_staff = encrypt(models.BooleanField(default=False))
	#is_active = encrypt(models.BooleanField(default=False))
	date_joined = encrypt(models.DateField(null=True))
	first_name = encrypt(models.CharField('',max_length=150,null=True))
	last_name = encrypt(models.CharField('',max_length=150,null=True))

class Story(models.Model):
	title = models.CharField('Story name',max_length=100) 
	text = models.TextField()
	img = models.ImageField(upload_to = 'images', default=None)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.title

class OTPmaster(models.Model):
	value = encrypt(models.CharField('',max_length=100))
	user = models.OneToOneField(to=User,on_delete=models.CASCADE)
