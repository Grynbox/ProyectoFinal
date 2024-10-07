from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("",views.login_usuario, name = "login"),
    #URLs departamento operaciones
    path('home_operaciones/',views.home_operaciones, name='home_operaciones'),    
    path("home_operaciones/agregar_conductor/",views.agregar_conductor, name="agregar_conductor"),
    path('home_operaciones/agregar_vehiculo/',views.agregar_vehiculo, name="agregar_vehiculo"),
    path("home_operaciones/crear_reporte/",views.crear_reporte,name="crear_reporte"),
    path("home_operaciones/crear_reporte/<int:reporte_id>/",views.reporte_informacion,name="reporte_informacion"),
    #URLs departamento taller
    path("home_taller/", views.reportes_reparaciones, name ="reportes_reparaciones"),   
    path("home_taller/modificar_reporte/<int:id_reparacion>/",views.modificar_reporte, name = 'modificar_reporte') ,
    path("home_taller/modificar_reporte/<int:id_reparacion>/asignar_mecanico", views.asignar_mecanico, name = 'asignar_mecanico'),
    
]