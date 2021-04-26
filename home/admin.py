from django.contrib import admin

# Register your models here.
from .models import Show, User

admin.site.register(Show)

admin.site.register(User)
