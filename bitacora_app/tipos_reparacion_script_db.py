import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nombre_proyecto.settings')
django.setup()

from reporte_operaciones.models import TipoReparacion, Reparacion

# Primero, carga los tipos de reparación
with open('tipo_fallo.csv', 'r') as file:
    for line in file:
        tipo_reparacion_name = line.strip()
        TipoReparacion.objects.get_or_create(tipo_reparacion=tipo_reparacion_name)

# Luego, carga las reparaciones asociadas a sus tipos
with open('descripcion_fallo.csv', 'r') as file:
    for line in file:
        tipo_name, reparacion_desc = line.strip().split(',',1)
        
        # Busca o crea el tipo de reparación
        tipo_reparacion = TipoReparacion.objects.get(tipo_reparacion=tipo_name)
        
        # Crea la reparación asociada al tipo
        Reparacion.objects.get_or_create(tipo_reparacion=tipo_reparacion, reparacion=reparacion_desc)