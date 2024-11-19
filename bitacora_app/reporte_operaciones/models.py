from django.contrib.auth.models import AbstractUser


from django.db import models
from datetime import date 
from enum import Enum
from django.utils import timezone
from datetime import datetime, timedelta
class Departamento(Enum):
    OPERACIONES = 'Operaciones'
    TALLER = 'Taller'
    ALMACEN = 'Almacen'
    MECANICO = 'Mecanico'
    SUPERVISOR = 'Supervisor'
    JEFE_DEPARTAMENTO = 'Jefe Departamento'
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]    

class Especialidad(Enum):
    MOTOR = 'Motor'
    FRENOS = 'Frenos'
    SUSPENSION = 'Suspensión'
    ELECTRICO = 'Eléctrico'
    RESCATISTA = 'Rescatista'
    MUELLERO = 'Muellero'
    TEC_PINTOR = 'Técnico Pintor'
    PINTOR = 'Pintor'
    AYU_ELECTRICO = 'Ayudante Eléctrico'
    CARROCERO = 'Carrocero'
    AYU_CARROCERO = 'Ayudante Carrocero'
    SOLDADOR = 'Soldador'
    LAVADO_MOTOR = 'Lavadores de Motores'
    TEC_MEC_AUTOMOTRIZ = 'Técnico Mecánico Automotriz'
    TEC_ELEC_AUTOMOTRIZ = 'Técnico Electrico Automotriz'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]
    
class UsuarioAutocar(AbstractUser):
    departamento = models.CharField(
        max_length=20,
        choices=Departamento.choices()
    )
    especialidad = models.CharField(
        max_length=20,
        choices=Especialidad.choices(),
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name} "   
    def es_mecanico(self):
        return self.departamento == Departamento.MECANICO.name    


class ZonaVehiculos(Enum):
    NORTE = 'Norte'
    SUR = 'Sur'
    HOTELES = 'Hoteles'
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]        



class Conductor(models.Model):
    id_conductor = models.AutoField(primary_key=True)
    nombre_conductor = models.CharField(max_length=20)
    apellido_conductor = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.nombre_conductor} {self.apellido_conductor} "  


class TipoIngreso(Enum):
    CORRECTIVO = 'Correctivo'
    RESCATE = 'Rescate'
    PREVENTIVO = 'Preventivo'
    ACCIDENTE = 'Accidente'
    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]

class EstatusReporte(Enum):
    ACTIVO = 'Activo'
    SIN_ASIGNAR = 'Sin Asignar'
    TERMINADO = 'Terminado'
    SUSPENDIDO = 'Suspendido'
    
    
    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]        
class Vehiculos(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)  # Corrigiendo el error con primary_key
    numero_unidad = models.CharField(max_length=30)  # Agregar max_length
    modelo_unidad = models.CharField(max_length=30)
    año_unidad = models.CharField(max_length=30)
    zona_unidad = models.CharField(
        max_length=20,
        choices=ZonaVehiculos.choices()
    )
    kilometraje = models.IntegerField()
    def __str__(self):
        return f"{self.numero_unidad} {self.modelo_unidad}"  

class ReporteEntrada(models.Model):
    #Llave primaria
    id_reporte = models.AutoField(primary_key=True)
    

    #Llaves Foraneas
    conductor = models.ForeignKey('Conductor', on_delete=models.DO_NOTHING)
    reporte_usuario = models.ForeignKey('UsuarioAutocar',on_delete=models.DO_NOTHING)
    
    #Campos
    fecha_entrada = models.DateField(auto_now_add=True)
    fecha_terminado = models.DateField(null=True, blank=True, default=None)
    unidad = models.ForeignKey('Vehiculos', on_delete=models.DO_NOTHING)
    descripción_incidente = models.TextField(max_length=255)
    kilometraje_nuevo = models.IntegerField()

    def __str__(self):
        return str(self.id_reporte)

class ReporteReparacion(models.Model):
    id_reparacion = models.AutoField(primary_key=True)
    id_entrada = models.ForeignKey('ReporteEntrada',on_delete=models.CASCADE)
    id_reporte_mecanico = models.ManyToManyField('ReporteMecanico', blank=True)
    estacion = models.ForeignKey('Estacion',on_delete=models.PROTECT,default=None,null=True)
    tipo_entrada = models.CharField(
        max_length=20,
        choices=TipoIngreso.choices(),
        default='Sin Asignar'
    )
    estatus = models.CharField(
        max_length=20,
        choices=EstatusReporte.choices(),
        default = 'Pendiente',
    )

    def __str__(self):
        return str(self.id_reparacion)    

class MecanicosAsignados(models.Model):
    reporte_reparacion = models.ForeignKey('ReporteReparacion',on_delete=models.CASCADE)
    mecanico = models.ForeignKey('UsuarioAutocar',on_delete=models.CASCADE)
    #Condición para que solo sea una asignación del mecanico. No se le puede asignar dos veces al mecanico el mismo reporte
    class Meta:
        unique_together =('reporte_reparacion','mecanico')
    def __str__(self):
        return f"Reporte- {self.reporte_reparacion}, Mecanico- {self.mecanico}"

class ReporteMecanico(models.Model):
    id_mecanico = models.ForeignKey('UsuarioAutocar',on_delete=models.CASCADE)
    reporte_reparacion = models.ForeignKey('ReporteReparacion', on_delete=models.CASCADE, default=None)
    reparacion_selecionada = models.ManyToManyField('Reparacion',related_name='reparaciones',blank=True)
    estatus = models.CharField(default='Inactivo', max_length=15, blank=True,null=True)

    #tiempo de trabajo 
    fecha_inicio = models.DateField(default=None, blank=True,null=True)
    hora_inicio = models.TimeField(default=None,blank=True,null=True)    
    fecha_terminado = models.DateTimeField(default=None,blank=True,null=True)
    hora_termiando = models.TimeField(default=None,blank=True,null=True)
    tiempo_acumulado = models.DurationField(default=None,blank=True,null=True)
    def __str__(self):
        return f"{self.reporte_reparacion} {self.id}, {self.id_mecanico}"
    def iniciar_trabajo(self):
        ahora = timezone.now()
        self.fecha_inicio = ahora.date()
        self.hora_inicio = ahora.time()  
        self.save()
    def detener_trabajo(self):
        if self.hora_inicio:
            # Asegura que ambos objetos datetime sean "offset-aware"
            inicio = timezone.make_aware(
                timezone.datetime.combine(self.fecha_inicio, self.hora_inicio),
                timezone.get_current_timezone()
            )
            fin = timezone.now()  # Este ya es "offset-aware"
            
            # Inicializa tiempo_acumulado si es None
            if self.tiempo_acumulado is None:
                self.tiempo_acumulado = timedelta(0)
            
            # Calcula el tiempo transcurrido y lo acumula
            self.tiempo_acumulado += (fin - inicio)
            
            # Guarda los tiempos de terminación
            self.fecha_terminado = fin.date()
            self.hora_terminado = fin.time()
            
            # Limpia los campos de inicio para la próxima sesión de trabajo
            self.fecha_inicio = None
            self.hora_inicio = None
            self.save()    
class TipoReparacion(models.Model):
    tipo_reparacion = models.CharField(max_length=15)
    def __str__(self):
        return self.tipo_reparacion

class Reparacion(models.Model):
    tipo_reparacion = models.ForeignKey('TipoReparacion',on_delete=models.CASCADE)
    reparacion = models.CharField(max_length=30) 
    def __str__(self):
        return self.reparacion

DISPONIBILIDAD = [
    ('SI', 'Disponible'),
    ('NO', 'Ocupado')
]
class Estacion(models.Model):
    estado = models.CharField(max_length=15,choices=DISPONIBILIDAD, default='SI')
    num_estacion = models.IntegerField(blank=True,default=None)
    def __str__(self):
        return f"Estacion: {self.num_estacion} Estado : {self.get_estado_display()}"

class CantidadBuses(models.Model):
    zona_unidad = models.CharField(
        max_length=20,
        choices=ZonaVehiculos.choices()
    )
    cantidad = models.IntegerField(blank=True,default=0)
    def __str__(self):
        return f"{self.zona_unidad} : {self.cantidad}"

class PiezasAlmacen(models.Model):
    id_pieza = models.AutoField(primary_key=True)
    nombre_pieza = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)

class PiezasUsadas(models.Model):
    reporte_reparacion = models.ForeignKey('ReporteReparacion',on_delete=models.CASCADE)
    pieza = models.ForeignKey('PiezasAlmacen',on_delete=models.CASCADE)
    cantidad = models.IntegerField()
