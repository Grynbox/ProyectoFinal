import random
from datetime import datetime, timedelta
from reporte_operaciones.models import Vehiculos, Conductor, ReporteEntrada, ReporteReparacion, MecanicosAsignados, ReporteMecanico, UsuarioAutocar, Estacion, TipoReparacion, Reparacion

# Crear 10 vehículos
for i in range(1, 11):
    Vehiculos.objects.create(
        numero_unidad=f"{i}",
        modelo_unidad="Mercedes-Benz",
        año_unidad=str(random.randint(2010, 2020)),
        zona_unidad=random.choice(['NORTE', 'SUR', 'HOTELES']),
        kilometraje=random.randint(10000, 100000)
    )

# Crear conductores
nombres_conductores = ["Carlos", "Ana", "Miguel", "Lucia", "Pedro"]
apellidos_conductores = ["Ramírez", "López", "Martínez", "Gómez", "Díaz"]
for nombre, apellido in zip(nombres_conductores, apellidos_conductores):
    Conductor.objects.create(
        nombre_conductor=nombre,
        apellido_conductor=apellido
    )

# Crear reportes de entrada
descripciones_incidentes = ["Dejó de funcionar", "No enciende", "Clima no enfría", "Falla en luces"]
for i in range(20):
    ReporteEntrada.objects.create(
        conductor=Conductor.objects.order_by('?').first(),
        reporte_usuario=UsuarioAutocar.objects.filter(departamento='MECANICO').order_by('?').first(),
        fecha_entrada=datetime.now() - timedelta(days=random.randint(1, 180)),
        unidad=Vehiculos.objects.order_by('?').first(),
        descripcion_incidente=random.choice(descripciones_incidentes),
        kilometraje_nuevo=random.randint(10000, 100000)
    )

# Crear estaciones
for i in range(1, 11):
    Estacion.objects.create(
        num_estacion=i,
        estado=random.choice(['SI', 'NO'])
    )

# Crear tipos de reparación y reparaciones
tipo_reparaciones = ["Motor", "Frenos", "Clima"]
for tipo in tipo_reparaciones:
    tipo_rep = TipoReparacion.objects.create(tipo_reparacion=tipo)
    for _ in range(3):  # Tres reparaciones por tipo
        Reparacion.objects.create(
            tipo_reparacion=tipo_rep,
            reparacion=f"{tipo} - Reparación {random.randint(1, 3)}"
        )

# Crear reportes de reparación y asignar mecánicos
tipos_ingreso = ['Correctivo', 'Rescate', 'Accidente']
estatus_reporte = ['Activo', 'Sin Asignar', 'Terminado', 'Suspendido']
for i in range(20):
    reporte = ReporteReparacion.objects.create(
        id_entrada=ReporteEntrada.objects.order_by('?').first(),
        tipo_entrada=random.choice(tipos_ingreso),
        estatus=random.choice(estatus_reporte),
        estacion=Estacion.objects.filter(estado='SI').order_by('?').first()
    )
    
    # Asignar mecánicos y reportes mecánicos
    for _ in range(3):  # Tres mecánicos por reparación
        mecanico = UsuarioAutocar.objects.filter(departamento='MECANICO').order_by('?').first()
        ReporteMecanico.objects.create(
            id_mecanico=mecanico,
            reporte_reparacion=reporte,
            estatus="Activo",
            fecha_inicio=datetime.now() - timedelta(days=random.randint(1, 30)),
            tiempo_acumulado=timedelta(hours=random.randint(1, 8))
        )
