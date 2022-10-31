from django.db import models
from django.contrib.auth.models import User

class story(models.Model):
	title = models.CharField('Story name',max_length=100) 
	text = models.TextField()
	user = models.ManyToManyField(User)
	
	def __str__(self):
		return self.title

class OTPmaster(models.Model): # TODO encrypt this
	value = models.CharField('',max_length=100)
	user = models.OneToOneField(to=User,on_delete=models.CASCADE)