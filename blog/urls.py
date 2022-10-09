from django.urls import path

from . import views
from django.urls import include

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.log_in, name='login'),
	path("register", views.register_request, name="register"),
	path("accounts/", include("django.contrib.auth.urls")),
]
