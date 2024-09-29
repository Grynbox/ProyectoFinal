from django.contrib.auth.models import AbstractUser


from django.db import models
from datetime import date 
from enum import Enum

class Departamento(Enum):
    OPERACIONES = 'Operaciones'
    TALLER = 'Taller'
    ALMACEN = 'Almacen'
    REPARACION = 'Mecanico'
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]    
    
class UsuarioAutocar(AbstractUser):
    departamento = models.CharField(
        max_length=20,
        choices=Departamento.choices()
    )
    # Añadimos related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarioautocar_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarioautocar_permissions_set',
        blank=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name} "   
    

class ZonaVehiculos(Enum):
    NORTE = 'Norte'
    SUR = 'Sur'
    CENTRO = 'Centro'
    HOTELES = 'Hoteles'
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]        

class Vehiculos(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)  # Corrigiendo el error con primary_key
    numero_unidad = models.CharField(max_length=30)  # Agregar max_length
    modelo_unidad = models.CharField(max_length=30)
    año_unidad = models.CharField(max_length=30)
    zona_unidad = models.CharField(
        max_length=20,
        choices=ZonaVehiculos.choices()
    )
    kilometraje = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.numero_unidad} "  


class EspecialidadMecanico(Enum):
    CARROCERIA = 'Carroceria'
    ELECTRICO = 'Electrico'
    PINTURA = 'Pintura'
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]        

class Mecanico(models.Model):
    id_mecanico = models.AutoField(primary_key=True)
    nombre_mecanico = models.CharField(max_length=30)
    apellido_mecanico = models.CharField(max_length=30)
    especialidad_mecanico = models.CharField(
        max_length=25,
        choices=EspecialidadMecanico.choices()
    )
    def __str__(self):
        return f"{self.nombre_mecanico} {self.apellido_mecanico}"   


class Conductor(models.Model):
    id_conductor = models.AutoField(primary_key=True)
    nombre_conductor = models.CharField(max_length=20)
    apellido_conductor = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.nombre_conductor} {self.apellido_conductor} "  

class ReporteEntrada(models.Model):
    #Llave primaria
    id_reporte = models.AutoField(primary_key=True)

    #Llaves Foraneas
    conductor = models.ForeignKey('Conductor', on_delete=models.DO_NOTHING)
    reporte_usuario = models.ForeignKey('UsuarioAutocar', on_delete=models.DO_NOTHING)
    
    #Campos
    fecha_entrada = models.DateField(auto_now_add=True)
    fecha_terminado = models.DateField(null=True, blank=True, default=None)
    unidad = models.ForeignKey('Vehiculos', on_delete=models.DO_NOTHING)
    descripcion_incidente = models.CharField(max_length=255)
    kilometraje_nuevo = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id_reporte)

class TipoIngreso(Enum):
    CORRECTIVO = 'Correctivo'
    RESCATE = 'Rescate'
    PREVENTIVO = 'Preventivo'
    ACCIDENTE = 'Accidente'
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]    

class ReporteReparacion(models.Model):
    id_reparacion = models.AutoField(primary_key=True)
    id_reporte = models.ForeignKey('ReporteEntrada',on_delete=models.DO_NOTHING)
    tipo_ingreso = models.CharField(
        max_length=20,
        choices=TipoIngreso.choices()
    )
    def __str__(self):
        return self.id_reparacion    

class MecanicosAsignados(models.Model):
    reporte_reparacion = models.ForeignKey('ReporteReparacion',on_delete=models.CASCADE)
    mecanico = models.ForeignKey('Mecanico',on_delete=models.CASCADE)
    #Condición para que solo sea una asignación del mecanico. No se le puede asignar dos veces al mecanico el mismo reporte
    class Meta:
        unique_together =('reporte_reparacion','mecanico')

class ReporteMecanico(models.Model):
    id_mecanico = models.ForeignKey('Mecanico',on_delete=models.CASCADE)
    fecha_entrada = models.DateField(auto_now_add=True)
    hora_inicio = models.DateField(default=None)    
    fecha_terminado = models.DateTimeField(default=None)
    hora_termiando = models.DateTimeField(default=None)
    diagnosito_mecanico = models.CharField(max_length=255)
    tiempo_acumulado = models.CharField(max_length=100)


class PiezasRepuesto(models.Model):
    id_pieza = models.AutoField(primary_key=True)
    nombre_pieza = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)

class PiezasReparacion(models.Model):
    reporte_reparacion = models.ForeignKey('ReporteReparacion',on_delete=models.CASCADE)
    pieza = models.ForeignKey('PiezasRepuesto',on_delete=models.CASCADE)
    cantidad = models.IntegerField()