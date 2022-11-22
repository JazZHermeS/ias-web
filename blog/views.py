from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import RedirectView
from .forms import NewUserForm, UserUpdateForm, UserLoginForm, StoryUploadForm
from .models import Story, OTPmaster, User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages import get_messages
import pyotp
from django.db import models
import hashlib
from .settings import HASH_SALT, MEDIA_ROOT
import datetime



@login_required (login_url="/login/")
def profile(request, userstring):
	uid = User.objects.get(username=userstring) # TODO read permissions
	return render(request, "blog/profile.html",{"user": uid, "current_user": request.user})


def lockout(request, credentials, *args, **kwargs):
	current_datetime = datetime.datetime.now().strftime('%H:%M:%S')
	messages.error(request, ("Too many login attempts, wait 5 minutes before trying again"))
	return redirect('/login')


@login_required (login_url="/login/")
def settings(request):
	if request.method == "POST":
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, "Profile successfully updated." )
			#return render(request, "blog/main_page.html", {})
			#return redirect("/")
		else:
			messages.error(request, "Error: Invalid fields." )
			return redirect("/settings")
	else:
		form = UserUpdateForm()
		# messages.error(request, "Profile NOT updated. Invalid information.")

	try:
		master = OTPmaster.objects.get(user=request.user)
		qr = pyotp.totp.TOTP(master.value).provisioning_uri(name=request.user.email, issuer_name='Story Time')
	except OTPmaster.DoesNotExist:
		qr = None

	return render(request, "blog/settings.html",{"form": form, "user": request.user, "qr": qr})

@login_required (login_url="/login/")
def update_otp(request):
	if request.method == "POST":
		if request.POST["enable"] == "1":
			code = pyotp.random_base32()
			OTPmaster.objects.create(value=code,user=request.user)
		else:
			OTPmaster.objects.get(user=request.user).delete()
	messages.success(request, "Your OTP preferences have been updated." )
	return redirect("/settings")

def log_in(request):
	if request.method == "POST":
		username=request.POST["username"]
		password=request.POST["password"]
		user=authenticate(request, username=username, password=password)

		if user != None:
			try:
				master = OTPmaster.objects.get(user=user)
				totp = pyotp.totp.TOTP(master.value)
			except OTPmaster.DoesNotExist:
				totp = None

			if (totp != None) and not(totp.verify(request.POST.get("otp","").replace(" ",""))):
				messages.error(request, ("Error: OTP validation failed, try again"))
				return redirect('/login')

			login(request, user)
			messages.success(request, "Successfully logged in." )
			return redirect('/')
		else:
			messages.error(request, ("Error: There was an error loging in"))
			return redirect('/login')
	else:
		form = UserLoginForm()
		return render(request, 'registration/login.html', {"form": form})


@login_required (login_url="/login/")
def password_change(request):
	user = request.user
	if request.method == "POST":
		old_password = request.POST['old_password'].strip()
		new_password = request.POST['new_password1'].strip()
		if old_password == new_password:
			messages.error(request, ("Error: The new password is the same as the old password."))
			return redirect('/password_change')

		form = PasswordChangeForm(user, request.POST)
		if form.is_valid():
			user_form = form.save()
			update_session_auth_hash(request, user_form)
			messages.success(request, "Your password has been changed." )
			#return render(request, "blog/main_page.html", {})
			return redirect('/')
		else:
			messages.error(request, ("Error: The form is not valid"))
			return redirect('/password_change')
	else:
		form = PasswordChangeForm(user)
		return render(request, 'blog/new_password.html', {'form': form})

@login_required (login_url="/login/")
def profile_delete(request):
	request.user	
	template = loader.get_template("blog/profile_delete.html")
	return render(request, "blog/profile_delete.html", {})

@login_required (login_url="/login/") ## TODO
def profile_final_delete(request):
	try:
		user = request.user
		user.delete()
		messages.success(request, "Your account has been deleted." )
		return redirect('/')

	except Exception as e:
		return render(request, '/',{'err':e.message})

@login_required (login_url="/login/")
def log_out(request):
	logout(request)
	messages.success(request, "Successfully logged out." )
	return redirect('/')


def register_request(request):
	if request.method == "POST":
		email = request.POST['email'].strip()

		m = hashlib.sha256()
		m.update((HASH_SALT+email).encode('utf-8')) # The hash of the email is stored with a salt
		hashed_email = m.hexdigest()

		if User.objects.filter(hashed_email=hashed_email).exists():
			messages.error(request, "Error: Your email belongs to another user!" )
			return redirect("/register")

		form = NewUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		else:
			messages.error(request, "Error: Invalid fields." )
			return redirect("/register")
	else:
		form = NewUserForm()
		return render(request, "registration/register.html",{"form": form})


def home(request):
	request.user
	story_list = Story.objects.all()
	template = loader.get_template("blog/home.html")
	return render(request, "blog/home.html", {'story_list':story_list})

def GDPR(request):
	template = loader.get_template("blog/GDPR.html")
	return render(request, "blog/GDPR.html", {})

@login_required (login_url="/login/")
def new_story(request):
	if request.method == "POST":
		form = StoryUploadForm(request.POST, request.FILES)
		if form.is_valid():
			new_story = form.save(commit=False)
			new_story.user = request.user
			new_story.save()
			return redirect("/")

	else:
		form = StoryUploadForm()

	return render(request, "blog/new_story.html", {'form':form})

# new
def uploadView(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
            form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


@login_required (login_url="/login/")
def my_stories(request):
	my_stories_list = Story.objects.all().filter(user=request.user)
	if my_stories_list.count() == 0:
		has_story = False
	else:
		has_story = True
	return render(request, "blog/my_stories.html", {'my_stories_list':my_stories_list, 'has_story':has_story})

@login_required(login_url="/login/")
def story_details(request):
	story_id = request.GET.get('st')
	story = Story.objects.get(pk=story_id)

	return render(request, "blog/details.html", {"story":story})
