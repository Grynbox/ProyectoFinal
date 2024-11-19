from .models import ReporteReparacion,ReporteMecanico,UsuarioAutocar,ReporteEntrada,Vehiculos,Conductor,MecanicosAsignados,ReporteMecanico,TipoReparacion,Reparacion,Estacion,CantidadBuses

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UsuarioAutocarCreacionForm, UsuarioAutocarCabioForm
# Register your models here.
from django import forms

class ReporteMecanicoForm(forms.ModelForm):
    class Meta:
        model = ReporteMecanico
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra el queryset de reparacion_seleccionada solo a las reparaciones que ya están asociadas
        if self.instance.pk:
            self.fields['reparacion_selecionada'].queryset = self.instance.reparacion_selecionada.all()
        else:
            self.fields['reparacion_selecionada'].queryset = Reparacion.objects.none()

@admin.register(ReporteMecanico)
class ReporteMecanicoAdmin(admin.ModelAdmin):
    form = ReporteMecanicoForm

admin.site.register(ReporteReparacion)
# admin.site.register(ReporteMecanico)
admin.site.register(ReporteEntrada)
admin.site.register(Vehiculos)
admin.site.register(Conductor)
admin.site.register(MecanicosAsignados)
admin.site.register(TipoReparacion)
admin.site.register(Reparacion)
admin.site.register(Estacion)
admin.site.register(CantidadBuses)
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
    fieldsets = UserAdmin.fieldsets + ((None,{"fields":("departamento","especialidad")}),)
    add_fieldsets = UserAdmin.add_fieldsets+ ((None,{"fields":("departamento","especialidad")}),)
admin.site.register(UsuarioAutocar,UsuarioAutocarAdmin)