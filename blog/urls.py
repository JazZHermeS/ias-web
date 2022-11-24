from django.urls import include, path
from . import views
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls.conf import include, re_path  
from django.conf import settings  
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static  
#from django.conf.urls import url
from django.views.static import serve

handler404 = views.handle404
handler500 = views.handle500

urlpatterns = [
	path('admin/', admin.site.urls),
	path("", views.home, name="home"),
	path("login/", views.log_in, name="login"),
	path("register/", views.register_request, name="register"),
	path("", include("django.contrib.auth.urls")),
	path("my_stories/", views.my_stories, name="my_stories"),
	path("new_story", views.new_story, name="new_story"),
	path("profile/<str:userstring>", views.profile, name="profile"),
	path("settings", views.settings, name="settings"),
	path("GDPR", views.GDPR, name="GDPR"),
	path("update_otp", views.update_otp, name="update_otp"),
	path("password_change", views.password_change, name="password_change"),
	path("profile_delete", views.profile_delete, name="profile_delete"),
	path("profile_final_delete", views.profile_final_delete, name="profile_final_delete"),
	re_path(r'^story_details/\?st=[0-9]+', views.story_details, name="story_details"),
	re_path('story_details/', views.story_details, name="story_details"),
	re_path('edit_story/', views.edit_story, name="edit_story"),
	re_path('delete_story/', views.delete_story, name="delete_story"),
	re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
	re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
