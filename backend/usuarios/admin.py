from django.contrib import admin

from django.contrib.auth.models import  Group



from django_rest_passwordreset.models import ResetPasswordToken
from .models import  User, Teacher, Client,Case2

# Register your models here.

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Client)
#admin.site.register(Case)
admin.site.register(Case2)
admin.site.unregister(Group)

#admin.site.unregister(ResetPasswordToken)
