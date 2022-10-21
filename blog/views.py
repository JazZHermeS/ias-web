from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.generic import RedirectView
from .forms import NewUserForm
from .models import ToDoList, Item
from .forms import NewUserForm

def profile(request, id):
	ls = ToDoList.objects.get(id=id) 
	return HttpResponse("<h1>%s</h1>"%id)

def log_in(request):
	template = loader.get_template('registration/login.html')
	return HttpResponse(template.render())

def register_request(request):
	#template = loader.get_template('registration/register.html')
	#return HttpResponse(template.render())	
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			form.save()
			#login(request, user)
			#messages.success(request, "Registration successful." )
			#return render(request, "blog/main_page.html", {})
			#messages.error(request, "Unsuccessful registration. Invalid information.")
		return redirect("/")
	else:
		form = NewUserForm()
	return render(request, "register/register.html",{"form": form})

def home(request):
	template = loader.get_template("main_page.html")
	return render(request, "blog/main_page.html", {})

def new_story(request):
	template = loader.get_template("new_story.html")
	return HttpResponse(template.render())

def my_stories(request):
	template = loader.get_template("my_stories.html")
	return HttpResponse(template.render())
