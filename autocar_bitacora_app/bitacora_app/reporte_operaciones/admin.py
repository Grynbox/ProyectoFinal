from django.contrib import admin
from .models import ReporteReparacion,ReporteMecanico,UsuarioAutocar,ReporteEntrada,Mecanico,Vehiculos,Conductor

# Register your models here.

admin.site.register(ReporteMecanico)
admin.site.register(ReporteReparacion)
admin.site.register(UsuarioAutocar)
admin.site.register(ReporteEntrada)
admin.site.register(Vehiculos)
admin.site.register(Conductor)