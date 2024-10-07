from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#Modelos
from .models import ReporteEntrada, UsuarioAutocar, Conductor, Vehiculos, MecanicosAsignados, ReporteReparacion
from django.contrib.auth.admin import UserAdmin

#Forms para usuario operaciones
class CrearReporteNuevo(forms.ModelForm):
    class Meta:
        model = ReporteEntrada
        fields =['id_reporte', 'unidad','conductor', 'descripcion_incidente' , 'kilometraje_nuevo']

class AgregarConductor(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['nombre_conductor','apellido_conductor']

class AgregarVehiculo(forms.ModelForm):
    class Meta:
        model = Vehiculos
        fields= ['numero_unidad','modelo_unidad','año_unidad','zona_unidad','kilometraje']

class ModificarReporte(forms.ModelForm):
    class Meta:
        model = ReporteReparacion
        fields = ['tipo_entrada','estatus']
        
# Cambia el formulario de la pagina admin
class UsuarioAutocarCreacionForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UsuarioAutocar
        fields = UserCreationForm.Meta.fields + ("departamento",)

class UsuarioAutocarCabioForm(UserChangeForm):
    class Meta:
        model = UsuarioAutocar
        fields= UserChangeForm.Meta.fields

# ASIGNAR MECANICOS

class AsignarMecanico(forms.ModelForm):
    class Meta:
        model = MecanicosAsignados
        fields = ['reporte_reparacion','mecanico']