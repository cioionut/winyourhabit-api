from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from winyourhabit_api.models import User, HabitGroup

admin.site.register(User, UserAdmin)

admin.site.register(HabitGroup)