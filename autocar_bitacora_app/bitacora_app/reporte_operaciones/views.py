from django.http import HttpResponse, Http404,HttpResponseRedirect
#autenticación de usuario
from django.contrib.auth.decorators import login_required
from django.template import loader
from .models import ReporteEntrada
from django.shortcuts import render
from .forms import CrearReporteNuevo


def taller_reporte(request):
    lista_reporte = ReporteEntrada.objects.all()
    #template = loader.get.template("reporte_operaciones/index.html")
    return render(request,'reporte_operaciones/taller.html',{'lista_reporte':lista_reporte})

def reporte_informacion(request,reporte_id):
    try:
        reporte = ReporteEntrada.objects.get(id_reporte=reporte_id)
    except:
        raise HTTP404("El reporte no existe")
    return render(request, 'reporte_operaciones/reporte.html' ,{'reporte':reporte})

@login_required  # Asegúrate de que el usuario esté autenticado antes de crear el reporte
def crear_reporte(request):
    if request.method == "POST":
        form = CrearReporteNuevo(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.reporte_usuario = request.user
            reporte.save()
        #return HttpResponseRedirect("/%i" %form.id_reporte)
    else:
        form = CrearReporteNuevo()

    return render(request,'reporte_operaciones/crear_reporte.html',{"form":form})
