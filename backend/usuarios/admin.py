from django.contrib import admin
from .models import Pregunta, Opcion, Respuesta
from .models import Case, User, Teacher, Client
# Register your models here.

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Client)
admin.site.register(Case)

class OpcionInline(admin.TabularInline):
    model = Opcion
    fk_name = 'pregunta'
    extra = 1

class RespuestaInline(admin.TabularInline):
    model = Respuesta
    fk_name = 'pregunta'
    extra = 1


class PreguntaAdmin(admin.ModelAdmin):
    fields = ('codigo', 'texto', 'orden',)
    list_display = ('codigo', 'texto', 'orden',)
    list_editable = ('orden',)

    inlines = [OpcionInline, RespuestaInline]


admin.site.register(Pregunta, PreguntaAdmin)