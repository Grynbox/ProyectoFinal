from django.http import HttpResponse 
from django.template import loader
from .models import ReporteEntrada


def index(request):
    lista_reportes = ReporteEntrada.objects() 
    reportes = ",".join([r.conductor for r in lista_reportes])
    template = loader.get.template("reporte_operaciones/index.html")
    contexto = {
        "lista_reportes":lista_reportes,
    }
    return HttpResponse(template.render(contexto,request))

#def ReportesEntrada(request,reporte_entrada_id):
    #respuesta = "Estas viendo el reporte numero %s"
    #return HttpResponse(respuesta % reporte_entrada_id)
