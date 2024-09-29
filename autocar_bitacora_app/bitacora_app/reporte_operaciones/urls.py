from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
    path("crear_reporte/",views.crear_reporte,name="crear_reporte"),
    path("crear_reporte/<int:reporte_id>/",views.reporte_informacion,name="reporte_informacion"),
    path("taller_reporte/", views.taller_reporte, name ="taller_reporte"),    
    
    
]