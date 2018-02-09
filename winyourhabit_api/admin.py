from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from winyourhabit_api.models import User, HabitGroup, Proof, Objective, Vote

admin.site.register(User, UserAdmin)

admin.site.register(HabitGroup)
admin.site.register(Proof)
admin.site.register(Objective)
admin.site.register(Vote)

