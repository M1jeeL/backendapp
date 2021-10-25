from django.contrib import admin

from .models import Case, User, Teacher, Client,Case2
# Register your models here.

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Client)
#admin.site.register(Case)
admin.site.register(Case2)