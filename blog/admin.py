from django.contrib import admin
#from .models import ToDoList
from .models import Story
from .models import User

#admin.site.register(ToDoList)
admin.site.register(Story)
admin.site.register(User)