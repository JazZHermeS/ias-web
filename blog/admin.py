from django.contrib import admin
#from .models import ToDoList
from .models import Story
from .models import User

class storyAdmin(admin.ModelAdmin):
    list_display = ["title", "text", "img"]

admin.site.register(Story, storyAdmin)
admin.site.register(User)
