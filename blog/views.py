from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import RedirectView
from .forms import NewUserForm, UserUpdateForm
#from .models import ToDoList, Item
from .models import story
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

@login_required (login_url="/login/")
def profile(request, username):
	if request.method == "POST":
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, "Profile successfully updated." )
			#return render(request, "blog/main_page.html", {})
			return redirect("/")
	else:
		form = UserUpdateForm()
		messages.error(request, "Profile NOT updated. Invalid information.")
	return render(request, "blog/profile.html",{"form": form, "user":request.user})

def log_in(request):
	if request.method == "POST":
		username=request.POST["username"]
		password=request.POST["password"]
		user=authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.success(request, ("There was an error loging in, try again"))
			return redirect('/login')
	else:
		return render(request, 'register/login.html', {})


@login_required (login_url="/login/")
def password_change(request):
	user = request.user
	if request.method == "POST":
		form = PasswordChangeForm(user, request.POST)
		if form.is_valid():
			user_form = form.save()
			update_session_auth_hash(request, user_form)
			messages.success(request, "Your password has been changed." )
			#return render(request, "blog/main_page.html", {})
			return redirect('/')
	else:
		form = PasswordChangeForm(user)
		return render(request, 'blog/new_password.html', {'form': form})


@login_required (login_url="/login/")
def log_out(request):
	logout(request)
	return redirect('home')


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "Registration successful." )
			#return render(request, "blog/main_page.html", {})
			return redirect("/")
	else:
		form = NewUserForm()
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render(request, "register/register.html",{"form": form})


def home(request):
	request.user
	story_list = story.objects.all()
	template = loader.get_template("main_page.html")
	return render(request, "blog/main_page.html", {'story_list':story_list})


@login_required (login_url="/login/")
def new_story(request):
	request.user
	template = loader.get_template("new_story.html")
	return HttpResponse(template.render())


@login_required (login_url="/login/")
def my_stories(request):
	template = loader.get_template("my_stories.html")
	return HttpResponse(template.render())

