from django import forms
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['email']

