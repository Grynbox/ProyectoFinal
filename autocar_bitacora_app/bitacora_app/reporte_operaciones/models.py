from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date 
from enum import Enum

class Departamento(Enum):
    OPERACIONES = 'Operaciones'
    TALLER = 'Taller'
    ALMACEN ='Almacen'
    REPARACION = 'Mecanico'
    

class UsuarioAutocar(AbstractUser):
    departamento = models.CharField(
        max_length=20,
        choices=[(tag,tag.value)for tag in Departamento]
        )
class ZonaVehiculos(Enum):
    NORTE = 'Norte'
    SUR = 'Sur'
    CENTRO = 'Centro'

class Vehiculos(models.Model):
    id_vehiculo = models.AutoField()
    numero_unidad = models.CharField(primary_key=True)
    modelo_unidad = models.CharField(max_length=30)
    ano_unidad = models.CharField(max_length=30)
    zona_unidad = models.CharField(
        max_length='20',
        choices=[(tag,tag.value) for tag in ZonaVehiculos]
    )
class EspecialidadMecanico(Enum):
    CARROCERIA = 'Carroceria'
    ELECTRICO = 'Electrico'
    PINTURA = 'Pintura'

class Mecanico(models.Model):
    id_mecanico = models.AutoField(primary_key=True)
    nombre_mecanico = models.CharField(max_length=30)
    apellido_mecanico = models.CharField(max_length=30)
    especialidad_mecanico = models.CharField(
        max_length=15,
        choices=[(tag,tag.value)for tag in EspecialidadMecanico]
    )
class Conductor(models.Model):
    id_conductor = models.AutoField(primary_key=True)
    nombre_conductor = models.CharField(max_length=20)
    apellido_conductor = models.CharField(max_length=20)

class ReporteEntrada(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    #Cuando crea el reporte se guarda la fecha de creación
    fecha_entrada = models.DateField(auto_now_add=True)
    fecha_terminado = models.DateField(default= None)
    unidad = models.ForeignKey(Vehiculos)
    conductor = models.ForeignKey(Conductor)
    reporte_usuario = models.ForeignKey(UsuarioAutocar)