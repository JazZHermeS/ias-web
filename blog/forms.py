from django import forms
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import User, Story
from .settings import HASH_SALT
import hashlib

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		
		m = hashlib.sha256()
		m.update((HASH_SALT+user.email).encode('utf-8'))
		hashed_email = m.hexdigest()	
		
		user.hashed_email = hashed_email
		if commit:
			user.save()
		return user

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['email']

class UserLoginForm(forms.ModelForm):
	otp = forms.CharField(required=False)
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ["username", "password"]

class StoryUploadForm(forms.ModelForm):
	class Meta:
		model = Story
		fields = ['title', 'text', 'img']

	title = forms.CharField(max_length=100, required=True, widget=forms.TextInput, label="Title:")
	text = forms.CharField(max_length=5000, required=True, widget=forms.Textarea, label="Write your story here!")
	img = forms.ImageField(required=False, label="You can post a picture if you want!", widget=forms.FileInput)
		


