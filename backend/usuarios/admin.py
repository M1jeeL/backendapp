from django.contrib import admin
from django.contrib.admin import sites
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import  Group

from allauth.account.models import EmailAddress
from django.contrib.sites.models import Site

from django_rest_passwordreset.models import ResetPasswordToken
from .models import  User, Teacher, Client,Case

# Register your models here.
class ProfileUsers(admin.ModelAdmin):
    list_display = ("is_client",  "is_teacher","email")
    list_filter = ("is_client",  "is_teacher","email")
class ProfileClient(admin.ModelAdmin):
    list_display = ("rut","phone","created_at")
    list_filter = ("rut","phone","created_at")
class ProfileTeacher(admin.ModelAdmin):
    list_display = ("rut","phone","expertise","created_at")
    list_filter = ("rut","phone","expertise","created_at")

class ProfileCase(admin.ModelAdmin):
    list_display = ("type_status","status","chat_preference","created_at","finished_at")
    list_filter = ("type_status","status","chat_preference","created_at","finished_at")     

admin.site.register(User,ProfileUsers)
admin.site.register(Teacher,ProfileTeacher)
admin.site.register(Client,ProfileClient)
#admin.site.register(Case)
admin.site.register(Case,ProfileCase)
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(ResetPasswordToken)
admin.site.unregister(EmailAddress)