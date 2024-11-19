from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("",views.login_usuario, name = "login"),
    path('logout/', views.logout_view, name='logout'),
    #URLs departamento operaciones
    path('home_operaciones/',views.home_operaciones, name='home_operaciones'),    
    path("agregar_conductor/",views.agregar_conductor, name="agregar_conductor"),
    path('agregar_vehiculo/',views.agregar_vehiculo, name="agregar_vehiculo"),
    path("crear_reporte/",views.crear_reporte,name="crear_reporte"),
    path("crear_reporte/<int:reporte_id>/",views.reporte_informacion,name="reporte_informacion"),
    
    #URLs departamento taller
    path("home_taller/", views.reportes_reparaciones, name ="reportes_reparaciones"),   
    path("home_taller/modificar_reporte/<int:id_reparacion>/",views.modificar_reporte, name = 'modificar_reporte') ,
    #URLs mecanicos
    path("home_mecanico/", views.home_mecanico, name ="home_mecanico"),
    path('crear_reporte_mecanico/<int:id_reparacion>/',views.crear_reporte_mecanico,name='crear_reporte_mecanico'),
    path('cargar-reparaciones/', views.cargar_reparaciones, name='cargar_reparaciones'),
    #Supervisores 
    path('home_supervisor/', views.home_supervisor, name='home_supervisor'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    #Calculo de tiempo Mecanico
    path('iniciar_trabajo/<int:id_reporte_mecanico>/', views.iniciar_trabajo, name='iniciar_trabajo'),
    path('detener_trabajo/<int:id_reporte_mecanico>/', views.detener_trabajo, name='detener_trabajo'),

    #Dashboar
    path('home_dashboard/',views.dashboard_view_uno, name = 'dashboard_view_uno'),
    path('home_dashboard_dos/',views.dashboard_view_dos, name = 'dashboard_view_dos')
]