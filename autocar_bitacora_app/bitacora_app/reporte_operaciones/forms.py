from django import forms
from .models import ReporteEntrada

class CrearReporteNuevo(forms.ModelForm):
    class Meta:
        model = ReporteEntrada
        fields =[ 'unidad','conductor', 'descripcion_incidente' , 'kilometraje_nuevo']
    #fecha_entrada = format.DateField(auto_now_add=True)
    # unidad = forms.CharField(label="Numero Unidad", max_length=10)
    # conductor_nombre = forms.CharField(label="Nombre Conductor", max_length=30)
    # conductor_apellido = forms.CharField(label="Apellido Conductor", max_length=30)
    # descripcion_incidente = forms.CharField(label= "Descripcion", max_length=255)
    # kilometraje_nuevo = forms.CharField(label="Kilometraje",max_length=10)
