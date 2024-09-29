from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("reporte_operaciones/", include("reporte_operaciones.urls")),
    path('accounts/', include('django.contrib.auth.urls')),  # También incluye las URLs de autenticación
]
