from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #url de autenticación de django
    # path('', include('django.contrib.auth.urls')), 
    path('',include('reporte_operaciones.urls')),
    #aplicación principal

]
