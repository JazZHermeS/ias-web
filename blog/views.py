from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import RedirectView
from .forms import NewUserForm
#from .models import ToDoList, Item
from .models import story
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def profile(request, id):
	#ls = ToDoList.objects.get(id=id) 
	return HttpResponse("<h1>%s</h1>"%id)

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

def register_request(request):
	#template = loader.get_template('registration/register.html')
	#return HttpResponse(template.render())	
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

def new_story(request):
	request.user
	template = loader.get_template("new_story.html")
	return HttpResponse(template.render())

def my_stories(request):
	template = loader.get_template("my_stories.html")
	return HttpResponse(template.render())
