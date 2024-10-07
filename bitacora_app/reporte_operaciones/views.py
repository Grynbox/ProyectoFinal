#Modelos
from .models import ReporteEntrada,ReporteReparacion
#autenticación de usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
#Redirección de urls y renderización de templates
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, Http404,HttpResponseRedirect
#Formularios
from .forms import CrearReporteNuevo,AgregarConductor,AgregarVehiculo,MecanicosAsignados,ModificarReporte


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            # Verificación de que departamento es el usuario y redireccionar
            if user.departamento == "OPERACIONES":
                login(request,user)
                return HttpResponseRedirect("/home_operaciones")
            elif user.departamento == "TALLER":
                login(request,user)
                return HttpResponseRedirect("/home_taller")
            elif user.departamento == "ALMACEN":
                login(request,user)
                return HttpResponseRedirect("/home_almacen")
            elif user.departamento == "REPARACION":
                login(request,user)
                return HttpResponseRedirect("/home_mecanico")
        else:
            print('No hay usuario')
    return render(request, 'authenticate/login.html',{})

# Homepage y acciones para usuarios operaciones
@login_required
def home_operaciones(request):
    return render(request,'reporte_operaciones/home_operaciones.html')
@login_required
def agregar_conductor(request):
    button = "Agregar Conductor"

    if request.method == "POST":
        form = AgregarConductor(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/home_operaciones/")
    else:
        form = AgregarConductor()
    return render(request,'reporte_operaciones/crear_reporte.html',{"form":form,"button":button})

@login_required
def agregar_vehiculo(request):
    button = "Agregar Vehiculo"
    if request.method == "POST":
        form = AgregarVehiculo(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/home_operaciones/")
    else:
        form = AgregarVehiculo()
    return render(request,'reporte_operaciones/crear_reporte.html',{"form":form,"button":button})

@login_required  # Asegúrate de que el usuario esté autenticado antes de crear el reporte
def crear_reporte(request):
    button = "Crear Reporte"

    if request.method == "POST":
        #Verifica el formulario de llegada y crea nuevo reporte
        form = CrearReporteNuevo(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.reporte_usuario = request.user
            #Crear objeto reporte reparacion
            reporte.save()
            reporte_entrada = ReporteReparacion(id_entrada = reporte)
            reporte_entrada.save()
        return HttpResponseRedirect("./%i" %reporte.id_reporte)
    else:
        form = CrearReporteNuevo()

    return render(request,'reporte_operaciones/crear_reporte.html',{"form":form,"button":button})
@login_required
def reporte_informacion(request,reporte_id):
    try:
        reporte = ReporteEntrada.objects.get(id_reporte=reporte_id)
    except:
        raise HTTP404("El reporte no existe")
    return render(request, 'reporte_operaciones/reporte_id.html' ,{'reporte':reporte})


# Homepage y acciones departamento Taller
@login_required
def reportes_reparaciones(request):
    lista_reporte = ReporteReparacion.objects.all().order_by('-id_reparacion')
    return render(request,'reporte_operaciones/reportes_reparaciones.html',{'lista_reporte':lista_reporte})

@login_required
def modificar_reporte(request,id_reparacion):
    reporte = ReporteReparacion.objects.get(id_reparacion=id_reparacion)
    if request.method == 'POST':
        form = ModificarReporte(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("./%i" %id_reparacion)

    return render(request, 'reporte_operaciones/reporte_taller.html' ,{'reporte':reporte,'form':form})


# @login_required
# def modificar_reporte(request,id_reparacion):
#     try:
#         reporte = ReporteReparacion.objects.get(id_reparacion=id_reparacion)
#         if request.method == 'POST':
#             form = ModificarReporte(request.POST)
#             return HttpResponseRedirect("./%i" %id_reparacion)

#     except:
#         raise HTTP404("El reporte no existe")
#     return render(request, 'reporte_operaciones/reporte_taller.html' ,{'reporte':reporte})

@login_required
def asignar_mecanico(request,id_reparacion):
    if request.method == 'POST':
        form = MecanicosAsignados(request.POST)
        if form.is_valid():
            form.save()
            if form.is_valid():
                form.save()
        else:
            return HttpResponseRedirect("/home_taller/modificar_reporte/%i" %id_reparacion)
    else:
        form = MecanicosAsignados()
    return render(request,"reporte_operaciones/asignar_mecanico.html")

        
