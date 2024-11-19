#Modelos
from .models import ReporteEntrada,ReporteReparacion,Departamento,MecanicosAsignados,ReporteMecanico,Reparacion,Estacion,CantidadBuses,Especialidad
from django.contrib import messages
#autenticación de usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
#Redirección de urls y renderización de templates
from django.template import loader
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect,JsonResponse
#Formularios
from .forms import CrearReporteNuevo,AgregarConductor,AgregarVehiculo,AsignarMecanico,UsuarioAutocar,FiltroMecanicosForm,ModificarReporteReparacion,descripcion_reparacion,ReparacionSeleccionForm,EstacionForm,FiltroAsignarMecanicoForm,MecanicoForm
from django.core.paginator import Paginator
from django.db.models import Count,Q
from datetime import timedelta
from django.utils import timezone

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
            elif user.departamento == "MECANICO":
                login(request,user)
                return HttpResponseRedirect("/home_mecanico")
            elif user.departamento == "SUPERVISOR":
                login(request,user)
                return HttpResponseRedirect("/home_supervisor")
            elif user.departamento == "JEFE_DEPARTAMENTO":
                login(request,user)
                return HttpResponseRedirect("/home_dashboard")
        else:
            print('No hay usuario')
    return render(request, 'authenticate/login.html',{})

def logout_view(request):
    logout(request)
    return redirect('login') 

# Homepage y acciones para usuarios operaciones
@login_required
def home_operaciones(request):
    id_usuario = request.user.id
    reportes_entrada = ReporteEntrada.objects.filter(reporte_usuario = id_usuario).order_by('-id_reporte')
    reportes = reportes_entrada.filter(fecha_terminado__isnull=True)

    return render(request,'reporte_operaciones/home_operaciones.html',{'reportes': reportes})


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
    #Obtener el estatus de los parametros url
    estatus_filtro = request.GET.get('estatus',None)

    # lista_reporte = ReporteReparacion.objects.all().order_by('-id_reparacion')
    if estatus_filtro:
        lista_reporte = ReporteReparacion.objects.filter(estatus = estatus_filtro)
    else:
        lista_reporte = ReporteReparacion.objects.all()

    #Obtener Conteo
    estatus_count = ReporteReparacion.objects.values('estatus').annotate(total = Count('estatus'))
    # Crear un diccionario para manejar los diferentes estatus
    estatus_dict = {
        'Activo': 0,
        'Pendiente': 0,
        'Suspendido': 0,
        'Terminado': 0
    }
    for item in estatus_count:
        estatus_dict['estatus'] = item['total']

    paginador = Paginator(lista_reporte,'15')
    page_number = request.GET.get('page')
    page_obj = paginador.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'estatus_dic': estatus_dict,
        'estatus_filtro':estatus_filtro,
    }
    
    return render(request,'reporte_operaciones/home_taller.html',context)

from django.shortcuts import get_object_or_404

@login_required
def modificar_reporte(request, id_reparacion):
    # Obtener el reporte de reparación
    reporte = get_object_or_404(ReporteReparacion, id_reparacion=id_reparacion)
    
    # Formulario para modificar el estatus y tipo de entrada
    if request.method == "POST" and 'guardar_cambios' in request.POST:
        form = ModificarReporteReparacion(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los cambios han sido guardados correctamente')
            #Cambiar esl estado de la estación a desocupado
            if reporte.estatus == 'Terminado':
                reporte.id_entrada.fecha_terminado = timezone.now()
                reporte.id_entrada.save()
                estacion_seleccionada = reporte.estacion
                estacion_seleccionada.estado = 'SI'
                estacion_seleccionada.save()

            return redirect('modificar_reporte', id_reparacion=id_reparacion)
    else:
        form = ModificarReporteReparacion(instance=reporte)

    # Lógica del formulario de filtrado de mecánicos
    form_filtro = FiltroMecanicosForm(request.GET or None)
    mecanicos = UsuarioAutocar.objects.filter(departamento=Departamento.MECANICO.name)
    especialidad_seleccionada = None
    if 'filtrar' in request.GET and form_filtro.is_valid():
        especialidad_seleccionada = form_filtro.cleaned_data['especialidad']
        mecanicos = mecanicos.filter(especialidad=especialidad_seleccionada)

    # Lógica del formulario de asignación de mecánicos
    form_asignar = AsignarMecanico(request.POST or None)
    if especialidad_seleccionada:
        form_asignar.fields['mecanico'].queryset = mecanicos

    if request.method == "POST" and 'asignar' in request.POST and form_asignar.is_valid():
        asignacion = MecanicosAsignados()
        asignacion.reporte_reparacion = reporte
        asignacion.mecanico = form_asignar.cleaned_data['mecanico']
        asignacion.save()
        reporte_mecanico = ReporteMecanico()
        reporte_mecanico.id_mecanico = asignacion.mecanico
        reporte_mecanico.reporte_reparacion = reporte
        reporte_mecanico.save() 
        reporte.id_reporte_mecanico.add(reporte_mecanico) 
        messages.success(request, 'Mecánico asignado correctamente')
        return redirect('modificar_reporte', id_reparacion=id_reparacion)

    #Lógica para eliminar la asignación de Mecanico
    if request.method == "POST" and 'eliminar' in request.POST and form_asignar.is_valid():
        eliminar_mecanico = MecanicosAsignados.objects.get(reporte_reparacion = reporte.id_reparacion , mecanico = form_asignar.cleaned_data['mecanico'])
        eliminar_reporte_mecanico = ReporteMecanico.objects.get(reporte_reparacion = reporte.id_reparacion , id_mecanico = form_asignar.cleaned_data['mecanico'])
        eliminar_reporte_mecanico.delete()
        eliminar_mecanico.delete()
        messages.success(request, 'Mecánico eliminado correctamente')
        return redirect('modificar_reporte', id_reparacion=id_reparacion)

    #Asginación de Estacion
    form_estacion = EstacionForm(request.POST or None)
    if request.method == 'POST' and 'asignar_estacion' in request.POST:
        form_estacion = EstacionForm(request.POST)
        # Verifica si el formulario es válido
        if form_estacion.is_valid():
            # Obtiene la estación seleccionada
            estacion_seleccionada = form_estacion.cleaned_data['estacion']
            
            # Asigna la estación al reporte y guarda
            reporte.estacion = estacion_seleccionada
            reporte.save()

            # Cambia el estado de la estación a "Ocupado" y guarda
            estacion_seleccionada.estado = 'NO'
            estacion_seleccionada.save()

            messages.success(request, 'Estación asignada correctamente.')
            return redirect('modificar_reporte', id_reparacion=id_reparacion)
        else:
            # Muestra errores del formulario
            messages.error(request, 'Por favor, selecciona una estación válida.')

    #Eliminación de estación de asignación
    if request.method == 'POST' and 'eliminar_estacion' in request.POST:
        form_estacion = EstacionForm(request.POST)
        # Verifica si el formulario es válido
        if form_estacion.is_valid():
            # Obtiene la estación seleccionada
            estacion_seleccionada = form_estacion.cleaned_data['estacion']
            
            # Asigna la estación al reporte y guarda
            reporte.estacion = None
            reporte.save()

            # Cambia el estado de la estación a "Ocupado" y guarda
            estacion_seleccionada.estado = 'SI'
            estacion_seleccionada.save()

            messages.success(request, 'Estación asignada correctamente.')
            return redirect('modificar_reporte', id_reparacion=id_reparacion)
        else:
            # Muestra errores del formulario
            messages.error(request, 'Por favor, selecciona una estación válida.')

    # Mecanicos Asignados
    mecanicos_asignados = MecanicosAsignados.objects.filter(reporte_reparacion = reporte.id_reparacion)
    
    #logica para mostrar la tabla de mecanicos asignados
    context = {
        'reporte': reporte,
        'form': form,
        'form_filtro': form_filtro,
        'form_asignar': form_asignar,
        'form_estacion' : form_estacion,
        'mecanicos': mecanicos,
        'especialidad_seleccionada': especialidad_seleccionada,
        'mecanicos_asignados': mecanicos_asignados,
    }
    return render(request, 'reporte_operaciones/modificar_reporte_taller.html', context)


# Mecanicos
@login_required
def home_mecanico(request):
    id_mecanico = request.user.id
    reportes_asignados = MecanicosAsignados.objects.filter(mecanico=id_mecanico)
    reportes_reparacion = [asignacion.reporte_reparacion for asignacion in reportes_asignados]

    if request.method == 'POST':
        reporte_id = request.POST.get('reporte_id')  # Obtenemos el ID del reporte
        reporte = get_object_or_404(ReporteMecanico, id=reporte_id)
        form = ReporteMecanicoForm(request.POST, instance=reporte)

        if form.is_valid():
            form.save()
            return redirect('/home_mecanico/')
    else:
        form = descripcion_reparacion()

    return render(request, 'reporte_operaciones/home_mecanico.html', {'reportes': reportes_reparacion, 'form': form})


@login_required
def crear_reporte_mecanico(request, id_reparacion):
    reporte = get_object_or_404(ReporteReparacion, id_reparacion=id_reparacion)
    reporte_mecanico = ReporteMecanico.objects.get(id_mecanico=request.user.id,reporte_reparacion=reporte)
    if request.method == 'POST':
        form = ReparacionSeleccionForm(request.POST)
        tipo_reparacion_id = request.POST.get('tipo_reparacion')
        if tipo_reparacion_id:
            # Actualiza el queryset de 'reparacion' según el tipo de reparación seleccionado
            form.fields['reparacion'].queryset = Reparacion.objects.filter(tipo_reparacion_id=tipo_reparacion_id)
        
        if form.is_valid():

            # reporte_mecanico = form.save(commit=False)
            #Campos del reporte mecancio            
            # reporte_mecanico.id_mecanico = request.user
            reporte_mecanico.reporte_reparacion = reporte            
            reporte_mecanico.save()
            
            reporte_mecanico.reparacion_selecionada.set(form.cleaned_data['reparacion'])            
            
            #Asignar reporte mecanico a reporte reparacion 
            reporte.id_reporte_mecanico.add(reporte_mecanico)

            return  redirect("crear_reporte_mecanico", id_reparacion=id_reparacion)
    else:
        form = ReparacionSeleccionForm()
    reparacion_reportes = reporte.id_reporte_mecanico.all()
    contex = {
        'reporte':reporte,
        'form':form,
        'reparaciones' : reparacion_reportes
    }        
    return render(request,'reporte_operaciones/reporte_mecanico.html',contex)

def cargar_reparaciones(request):
    tipo_reparacion_id = request.GET.get('tipo_reparacion')
    reparaciones = Reparacion.objects.filter(tipo_reparacion=tipo_reparacion_id)
    reparaciones_data = [{'id': rep.id, 'nombre': rep.reparacion} for rep in reparaciones]
    return JsonResponse(reparaciones_data, safe=False)



#Supervisores

def home_supervisor(request):
    #Buscar reportes que esten activos o pendientes
    reportes = ReporteReparacion.objects.filter(estatus ='Activo') | ReporteReparacion.objects.filter(estatus ='Suspendido')
    contex  = {
        'reportes' : reportes
    }
    return render(request,'reporte_operaciones/home_sup_mecanico.html',contex)

def iniciar_trabajo(request, id_reporte_mecanico):
    reporte_mecanico = get_object_or_404(ReporteMecanico, id=id_reporte_mecanico)
    reporte_mecanico.estatus  = 'Activo'
    reporte_mecanico.iniciar_trabajo()
    return redirect('home_supervisor')  # Redirige a la vista que muestra los reportes

def detener_trabajo(request, id_reporte_mecanico):
    reporte_mecanico = get_object_or_404(ReporteMecanico, id=id_reporte_mecanico)
    reporte_mecanico.estatus  = 'Inactivo'

    reporte_mecanico.detener_trabajo()
    return redirect('home_supervisor')

#dashboard

def dashboard_view_uno(request):
    # Trabajos con más tiempo
    reportes_reparaciones = ReporteMecanico.objects.filter(Q(reporte_reparacion__estatus = "Activo") and ~Q(tiempo_acumulado = None)).order_by('-tiempo_acumulado')
    
    reportes_activos = ReporteReparacion.objects.filter(estatus='Activo').count()
    reportes_pendientes = ReporteReparacion.objects.filter(estatus='Pendiente').count()
    reportes_terminados= ReporteReparacion.objects.filter(estatus='Terminado').count()


    reportes = ReporteReparacion.objects.filter(estatus='Activo')

    # Contar los reportes por zonas
    Norte = reportes.filter(id_entrada__unidad__zona_unidad='NORTE').count()
    Sur = reportes.filter(id_entrada__unidad__zona_unidad='SUR').count()
    Z_hotelera = reportes.filter(id_entrada__unidad__zona_unidad='HOTELES').count()
    
    # Obtener la cantidad total de buses por zona
    buses_norte = CantidadBuses.objects.get(zona_unidad='NORTE')
    buses_sur = CantidadBuses.objects.get(zona_unidad='SUR')
    buses_hotelera = CantidadBuses.objects.get(zona_unidad='HOTELES')
    
    # Calcular los buses disponibles
    cantidad_buses_norte = buses_norte.cantidad - Norte
    cantidad_buses_sur = buses_sur.cantidad - Sur
    cantidad_buses_hotelera = buses_hotelera.cantidad - Z_hotelera
    
    # Calcular los porcentajes
    porcentaje_norte = (cantidad_buses_norte * 100) / buses_norte.cantidad
    porcentaje_sur = (cantidad_buses_sur * 100) / buses_sur.cantidad
    porcentaje_hotelera = (cantidad_buses_hotelera * 100) / buses_hotelera.cantidad
    
    estaciones = Estacion.objects.all()
    contex = {
        'reportes': reportes_reparaciones,
        'activos' : reportes_activos,
        'pendientes':reportes_pendientes,
        'terminados':reportes_terminados,
        'estaciones':estaciones,
        'norte':Norte,
        'sur':Sur,
        'hoteles':Z_hotelera,
    }
    return render(request,'reporte_operaciones/dashboard.html',contex)

def dashboard_view_dos(request):


    mecanico_departamento_promedio = {}
    
    for especialidad in Especialidad:
        mecanicos = UsuarioAutocar.objects.filter(especialidad=especialidad.name)
        if(mecanicos):
            for mecanico in mecanicos:
                reportes_mec = ReporteMecanico.objects.filter(Q(id_mecanico=mecanico) & ~Q(tiempo_acumulado = None))
                reportes_mecanicos_cant = reportes_mec.count()     
                tiempo_total = timedelta(0)
                for reportes in reportes_mec:
                    tiempo_total += reportes.tiempo_acumulado
                if reportes_mecanicos_cant >0:
                    promedio = tiempo_total/reportes_mecanicos_cant
                    mecanico_departamento_promedio[especialidad.value] = promedio

                else:
                    promedio = timedelta(0)

    labels = list(mecanico_departamento_promedio.keys())
    data = [round(t.total_seconds() / 3600, 2) for t in mecanico_departamento_promedio.values()]  # Convierte a horas

   
   
    # Lógica del formulario de filtrado de mecánicos
    form_filtro = FiltroMecanicosForm(request.GET or None)
    mecanicos = UsuarioAutocar.objects.filter(departamento=Departamento.MECANICO.name)
    especialidad_seleccionada = None
    if 'filtrar' in request.GET and form_filtro.is_valid():
        especialidad_seleccionada = form_filtro.cleaned_data['especialidad']
        mecanicos = mecanicos.filter(especialidad=especialidad_seleccionada)
    #Busqueda de reportes del mecanico
    promedio_mecanico = {}
    if mecanicos:
        for mecanico in mecanicos:
            reportes = ReporteMecanico.objects.filter(id_mecanico = mecanico)
            if reportes:
                reportes_cantidad = reportes.count()
                tiempo_trabajo_mecanico = timedelta(0)
                for reporte in reportes:
                    if reporte.tiempo_acumulado != None:
                        tiempo_trabajo_mecanico += reporte.tiempo_acumulado
                promedio = tiempo_trabajo_mecanico/reportes_cantidad
                promedio_mecanico[mecanico.first_name] = promedio
            else:
                tiempo_trabajo_mecanico = timedelta(0)
    labels_mecanico = list(promedio_mecanico)
    data_mecanico = [[round(t.total_seconds() / 3600, 2) for t in promedio_mecanico.values()]]

        # Vista para obtener los reportes de reparación junto con la información del mecánico y las reparaciones seleccionadas
    reportes_con_mecanico = ReporteReparacion.objects.select_related('id_entrada__unidad') \
        .prefetch_related('id_reporte_mecanico__id_mecanico', 'id_reporte_mecanico__reparacion_selecionada') \
        .order_by('id_entrada__unidad__numero_unidad')
    
    #Fitración de Mecanico
    mecanico_form = MecanicoForm(request.POST or None)
    tiempo_total = timedelta(0)  # Variable para almacenar el tiempo promedio
    
    if request.method == 'POST' and mecanico_form.is_valid():
        print(request.POST   )
        # Obtener el mecánico seleccionado
        mecanico = mecanico_form.cleaned_data['mecanico']
        print(mecanico)
        # Filtrar los reportes asociados a este mecánico
        reportes = ReporteMecanico.objects.filter(id_mecanico=mecanico)
        reportes_cantidad = reportes.count()
        tiempo_promedio = timedelta(0)
        if reportes:
            for reporte in reportes:
                if reporte.tiempo_acumulado != None:
                    tiempo_total += reporte.tiempo_acumulado
            tiempo_promedio = tiempo_total/reportes_cantidad        
             
        tiempo_total = round(tiempo_promedio.total_seconds()/ 3600, 2)               
        # Calcular el tiempo promedio de trabajo

    else:
        print(mecanico_form.errors)
        
    context ={
        'labels': labels,
        'data': data,
        'form_filtro': form_filtro,
        'labels_mecanico' : labels_mecanico,
        'data_mecanico' : data_mecanico,       
        'especialidad':especialidad_seleccionada,
        'reportes_con_mecanico' : reportes_con_mecanico,
        'mecanico_form':mecanico_form,
        'tiempo_promedio':tiempo_total 
    }
    return render(request,'reporte_operaciones/dashboard_dos.html',context)
