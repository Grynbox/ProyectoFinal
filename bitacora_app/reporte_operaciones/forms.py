from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#Modelos
from .models import ReporteEntrada, UsuarioAutocar, Conductor, Vehiculos, MecanicosAsignados, ReporteReparacion,Departamento,Especialidad,ReporteReparacion,ReporteMecanico,TipoReparacion,Reparacion,Estacion,ZonaVehiculos
from django.contrib.auth.admin import UserAdmin

#Forms para usuario operaciones
class CrearReporteNuevo(forms.ModelForm):
    class Meta:
        model = ReporteEntrada
        fields =['id_reporte', 'unidad','conductor', 'descripción_incidente' , 'kilometraje_nuevo']

        widgets = {
            'unidad' : forms.Select(attrs={'class':'form-control'}),
            'conductor' : forms.Select(attrs={'class':'form-control'}),
            'descripción_incidente' : forms.Textarea(attrs={'class':'form-control'}),
            'kilometraje_nuevo' : forms.TextInput(attrs={'class':'form-control'}),
        }

class AgregarConductor(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['nombre_conductor','apellido_conductor']

        widgets = {
            'nombre_conductor' : forms.TextInput(attrs={'class':'form-control'}),
            'apellido_conductor' : forms.TextInput(attrs={'class':'form-control'})
        }

class AgregarVehiculo(forms.ModelForm):
    class Meta:
        model = Vehiculos
        fields= ['numero_unidad','modelo_unidad','año_unidad','zona_unidad','kilometraje']

        widgets = {
            'numero_unidad' : forms.TextInput(attrs={'class':'form-control'}),
            'modelo_unidad' : forms.TextInput(attrs={'class':'form-control'}),
            'año_unidad' : forms.TextInput(attrs={'class':'form-control'}),
            'zona_unidad' : forms.Select(attrs={'class':'form-control'}),
            'kilometraje' : forms.TextInput(attrs={'class':'form-control'}),
        }

        
# Cambia el formulario de la pagina admin
class UsuarioAutocarCreacionForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UsuarioAutocar
        fields = ["username",
        "first_name",
        "last_name",
        "departamento",
        "especialidad",
        "password"]

class UsuarioAutocarCabioForm(UserChangeForm):
    class Meta:
        model = UsuarioAutocar
        fields= UserChangeForm.Meta.fields 
# FORMULARIO PARA MODIFICAR REPORTE_TALLER
class ModificarReporteReparacion(forms.ModelForm):
    class Meta:
        model = ReporteReparacion
        fields = ['tipo_entrada','estatus']

        widgets = {
            'tipo_entrada' : forms.Select(attrs={'class': 'form-control'}),
            'estatus' : forms.Select(attrs={'class': 'form-control'}),
        }
# ASIGNAR MECANICOS
class FiltroMecanicosForm(forms.Form):
    especialidad = forms.ChoiceField(
        choices=Especialidad.choices(),
        required=True,
        label="Especialidad",
        widget = forms.Select(attrs={'class':'form-control'})
    )

class AsignarMecanico(forms.ModelForm):
    mecanico = forms.ModelChoiceField(
        queryset=UsuarioAutocar.objects.filter(departamento=Departamento.MECANICO.name),
        widget= forms.Select(attrs={'class':'form-control'})
    )
    class Meta:
        model = MecanicosAsignados
        fields = ['mecanico']


class FiltroAsignarMecanicoForm(forms.Form):
    especialidad = forms.ChoiceField(
        choices=Especialidad.choices(),
        required=True,
        label="Especialidad",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'especialidad-select'})
    )
    mecanico = forms.ModelChoiceField(
        queryset=UsuarioAutocar.objects.none(),  # Inicialmente vacío, se llenará con AJAX
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'mecanico-select'})
    )

    def __init__(self, *args, **kwargs):
        especialidad_seleccionada = kwargs.pop('especialidad_seleccionada', None)
        super().__init__(*args, **kwargs)
        if especialidad_seleccionada:
            self.fields['mecanico'].queryset = UsuarioAutocar.objects.filter(
                departamento=Departamento.MECANICO.name, especialidad=especialidad_seleccionada
            )



class ReparacionSeleccionForm(forms.ModelForm):
    tipo_reparacion = forms.ModelChoiceField (
        label='Area de Reparación',
        queryset =  TipoReparacion.objects.all(),
        widget = forms.Select(attrs={'class':'form-control'})
    )
    reparacion = forms.ModelMultipleChoiceField(
        queryset=Reparacion.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class':'form-check'}),
        label="Reparacion"
    )

    class Meta:
        model = ReporteMecanico
        fields = ['reparacion_selecionada']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subreparacion = self.cleaned_data.get('subreparacion')
        if commit:
            instance.save()
        return instance     


class descripcion_reparacion(forms.ModelForm):
    REPARACION_CHOICES = [
        ('carroceria_imagen','Carrocería e Imagen'),
        ('cristales','Cristales'),
        ('direccion','Dirección'),  
        ('eje_delantero','Eje Delantero'),
        ('eje_trasero','Eje Trasero'),
        ('frenos','Frenos'),
        ('electrico','Electrico'),
        ('llantas','Llantas'),
        ('motor','Motor'),
        ('neumatico','Neumatico'),
        ('suspencion','Suspención'),
        ('transmision','Transmisión')
    ]
    tipo_reparacion = forms.ChoiceField(choices=REPARACION_CHOICES, label="Tipo de Reparación")
    subreparacion = forms.MultipleChoiceField(
        choices=[],  # Este campo se llenará dinámicamente
        widget=forms.CheckboxSelectMultiple,  # Usamos checkboxes para múltiples selecciones
        label="Sub-Reparación"
    )
    class Meta:
        model = ReporteMecanico
        fields = ['tipo_reparacion', 'subreparacion']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subreparacion = ','.join(self.cleaned_data.get('subreparacion'))
        if commit:
            instance.save()
        return instance     

class EstacionForm(forms.Form):
    estacion = forms.ModelChoiceField(
        queryset=Estacion.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})  # Opcional: agrega una clase CSS
    )
    

class MecanicoForm(forms.Form):
    mecanico = forms.ModelChoiceField(
        queryset=UsuarioAutocar.objects.filter(departamento='MECANICO'),
        label="Mecánico",
        empty_label="Seleccione un mecánico",
    )