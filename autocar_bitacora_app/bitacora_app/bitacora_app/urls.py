
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path("reporte_operaciones/", include("reporte_operaciones.urls")),
    path('admin/', admin.site.urls),
]
