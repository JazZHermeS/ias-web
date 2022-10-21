from django.urls import include, path
from . import views
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
	path('admin/', admin.site.urls),
	path("", views.home, name="home"),
	path("<int:id>", views.profile, name="profile"),
	path("register/", views.register_request, name="register"),
	path("", include("django.contrib.auth.urls")),
	path("my_stories", views.my_stories, name="my_stories"),
	path("new_story", views.new_story, name="new_story"),
]
