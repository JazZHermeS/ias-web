from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import RedirectView
from .forms import NewUserForm

def index(request):
	template = loader.get_template('index.html')
	return HttpResponse(template.render())

def log_in(request):
	template = loader.get_template('registration/login.html')
	return HttpResponse(template.render())

def register_request(request):
	#template = loader.get_template('registration/register.html')
	#return HttpResponse(template.render())	
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})
