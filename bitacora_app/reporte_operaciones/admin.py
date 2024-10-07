from .models import ReporteReparacion,ReporteMecanico,UsuarioAutocar,ReporteEntrada,Mecanico,Vehiculos,Conductor
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UsuarioAutocarCreacionForm, UsuarioAutocarCabioForm
# Register your models here.

admin.site.register(ReporteMecanico)
admin.site.register(ReporteReparacion)
admin.site.register(ReporteEntrada)
admin.site.register(Vehiculos)
admin.site.register(Conductor)

class UsuarioAutocarAdmin(UserAdmin):
    add_form = UsuarioAutocarCreacionForm
    form = UsuarioAutocarCabioForm
    model = UsuarioAutocar
    list_display =[
        "email",
        "username",
        "departamento",
        "is_staff",

    ]
    fieldsets = UserAdmin.fieldsets + ((None,{"fields":("departamento",)}),)
    add_fieldsets = UserAdmin.add_fieldsets+ ((None,{"fields":("departamento",)}),)
admin.site.register(UsuarioAutocar,UsuarioAutocarAdmin)