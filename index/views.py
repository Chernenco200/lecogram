
from asyncio.windows_events import NULL
from distutils.log import error
from telnetlib import theNULL
from xml.dom.expatbuilder import theDOMImplementation
from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate, logout
from index.forms import TODAY , LoginForm , ProveedorForm , EditarProveedorForm ,ClienteForm , EditarClienteForm , InventarioForm , ProductoForm, EditarProductoForm, IngresoForm , PersonalForm, EditarPersonalForm, EmpresaForm, DevolucionForm, PagosEgresoForm, ResponsableForm
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q , F 
from index.models import Egreso, ProductosIngreso, Proveedor, Cliente,Producto, Personal, Empresa , Ingreso, Devolucion, Ajuste, ProductosEgreso, MetodoPago, PagosEgreso
from django.http import JsonResponse , HttpResponse
from itertools import groupby
from datetime import date, datetime , timedelta
from django.template.loader import render_to_string
from django.views.generic import ListView
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from django.utils.decorators import method_decorator
HOY = datetime.today().strftime('%Y-%m-%d')
import os
import json
#from django.core import serializers
from django.utils.dateparse import parse_date
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.conf import settings
from django.db.models import Sum

#from bs4 import BeautifulSoup
#import requests

# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('Login')

def login_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('Index')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect ('Index')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login.html', context)



@login_required(login_url='Login')
def egresos_view(request):
    egresos = Egreso.objects.all()
    empresa = Empresa.objects.get(pk=1)
    moneda = empresa.moneda

    context = {
        'egresos': egresos,
        'moneda': moneda
    }

    return render(request, 'egresos.html', context)

@login_required(login_url='Login')
def ingresos_view(request):
    
    egresos = Ingreso.objects.all()
    num_programado = len(Ingreso.objects.filter(estado="Programado")) 
    num_espera = len(Ingreso.objects.filter(estado="En espera")) 
    num_proceso = len(Ingreso.objects.filter(estado="En proceso"))
    num_atrasado = len(Ingreso.objects.filter(estado="Atrasado"))
    num_realizado = len(Ingreso.objects.filter(estado="Realizado"))
    form_editar = IngresoForm()

    context = {
        'num_programado': num_programado,
        'num_espera': num_espera,
        'num_proceso': num_proceso,
        'num_atrasado': num_atrasado,
        'num_realizado': num_realizado,
        'egresos': egresos,
        'form_editar': form_editar,
    }

    return render(request, 'ingresos.html', context)

@login_required(login_url='Login')
def personal_view(request):
    
    form_personal = PersonalForm()
    form_editar_personal = EditarPersonalForm()
    personal = Personal.objects.all()
    num_personal = len(personal)

    context = {
        'form_personal': form_personal,
        'form_editar_personal': form_editar_personal,
        'personal': personal,
        'num_personal': num_personal
    }

    return render(request, 'personal.html', context)


@login_required(login_url='Login')
def add_personal_view(request):
    if request.POST:
        #print(request.POST)
        form = PersonalForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages.warning(request,"Personal ya agregado o datos incorrectos")
                return redirect('Personal')


    return redirect('Personal')


@login_required(login_url='Login')
def edit_personal_view(request):
    if request.POST:
        producto = Personal.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarPersonalForm(
            request.POST, request.FILES, instance=producto)
        if form.is_valid:
            form.save()

    return redirect('Personal')


@login_required(login_url='Login')
def delete_personal_view(request):
    if request.POST:
        personal = Personal.objects.get(pk=request.POST.get('id_personal_eliminar'))
        if personal.imagen:
            os.remove(personal.imagen.path)
        personal.delete()
        
    return redirect('Personal')


@login_required(login_url='Login')
def empresa_view(request):
    
    empresa = Empresa.objects.get(pk=1)
    form_empresa = EmpresaForm(instance=empresa)

    if request.POST:
        empresa = Empresa.objects.get(pk=1)
        form_empresa = EmpresaForm(
            request.POST, request.FILES, instance=empresa)
        if form_empresa.is_valid():
            form_empresa.save()
            form_empresa = EmpresaForm(instance=empresa)
            messages.info(request,"Cambios efectuados con éxito")
    context = {
        'form_empresa': form_empresa,
        'empresa': empresa
    }

    return render(request, 'empresa.html', context)

@login_required(login_url='Login')
def dashboard_view(request):

    fechas_ventas =[]
    subtototales_ventas =[]
    ventas = Egreso.objects.all().order_by('-id')[:10]
    ventas = reversed(ventas)
               
    for i in ventas:
        fechas_ventas.append(i.fecha_pedido)
        subtototales_ventas.append(float(i.total))

    #currentYear = datetime.now().year
    total_ventas = Egreso.objects.aggregate(Sum('total'))["total__sum"]
    total_compras = Ingreso.objects.aggregate(Sum('subtotalpiezas'))["subtotalpiezas__sum"]
    total_pedidos = Egreso.objects.all().count()
    total_devoluciones = Devolucion.objects.all().count()

    entregados = ProductosEgreso.objects.filter(entregado=True).aggregate(Sum('cantidad'))["cantidad__sum"]
    no_entregados = ProductosEgreso.objects.filter(entregado=False).aggregate(Sum('cantidad'))["cantidad__sum"]
    devoluciones = ProductosEgreso.objects.filter(devolucion=True).aggregate(Sum('cantidad'))["cantidad__sum"]
    ajustes = Ajuste.objects.all()

    if total_compras == None:
        total_compras = 0

    if total_ventas == None:
        total_ventas = 0
    
    print(fechas_ventas)
    context ={
        #'year': currentYear
        'total_ventas': total_ventas,
        'total_compras': total_compras,
        'total_pedidos': total_pedidos,
        'total_devoluciones': total_devoluciones,
        'fechas_ventas': fechas_ventas,
        'subtotales_ventas': subtototales_ventas,
        'entregados': entregados,
        'no_entregados': no_entregados, 
        'devoluciones': devoluciones, 
        'ajustes': ajustes
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='Login')
def resultData(request):
    if request.POST:
        data ={}
        try:
            fechas_ventas =[]
            subtotales_ventas =[]
            ventas = Egreso.objects.filter(fecha_pedido__gte = parse_date(request.POST["fechainicio"]), fecha_pedido__lte = parse_date(request.POST["fechafin"])).order_by('-id')[:10]
            ventas = reversed(ventas)
                    
            for i in ventas:
                fechas_ventas.append(i.fecha_pedido)
                subtotales_ventas.append(float(i.total))

            #currentYear = datetime.now().year
            total_ventas = Egreso.objects.filter(fecha_pedido__gte = parse_date(request.POST["fechainicio"]), fecha_pedido__lte = parse_date(request.POST["fechafin"])).aggregate(Sum('total'))["total__sum"]
            total_compras = Ingreso.objects.filter(fecha__gte = parse_date(request.POST["fechainicio"]), fecha__lte = parse_date(request.POST["fechafin"])).aggregate(Sum('subtotalpiezas'))["subtotalpiezas__sum"]
            total_pedidos = Egreso.objects.filter(fecha_pedido__gte = parse_date(request.POST["fechainicio"]), fecha_pedido__lte = parse_date(request.POST["fechafin"])).count()
            total_devoluciones = Devolucion.objects.filter(fecha__gte = parse_date(request.POST["fechainicio"]), fecha__lte = parse_date(request.POST["fechafin"])).count()

            entregados = ProductosEgreso.objects.filter(entregado=True, egreso__fecha_pedido__gte = parse_date(request.POST["fechainicio"]), egreso__fecha_pedido__lte = parse_date(request.POST["fechafin"])).aggregate(Sum('cantidad'))["cantidad__sum"]
            no_entregados = ProductosEgreso.objects.filter(entregado=False, egreso__fecha_pedido__gte = parse_date(request.POST["fechainicio"]), egreso__fecha_pedido__lte = parse_date(request.POST["fechafin"])).aggregate(Sum('cantidad'))["cantidad__sum"]
            devoluciones = ProductosEgreso.objects.filter(devolucion=True, egreso__fecha_pedido__gte = parse_date(request.POST["fechainicio"]), egreso__fecha_pedido__lte = parse_date(request.POST["fechafin"])).aggregate(Sum('cantidad'))["cantidad__sum"]

            ajustes = Ajuste.objects.filter(fecha__gte = parse_date(request.POST["fechainicio"]), fecha__lte = parse_date(request.POST["fechafin"]))
            cantidad_registrada = []
            cantidad_real = []
            key_productos = []

            for i in ajustes:
                cantidad_registrada.append(float(i.cantidad_registrada))
                cantidad_real.append(float(i.cantidad_real))
                key_productos.append(i.producto.descripcion)


            if total_compras == None:
                total_compras = 0

            if total_ventas == None:
                total_ventas = 0
            
            data["fechas_ventas"] = fechas_ventas
            data["subtotales_ventas"] = subtotales_ventas
            data["entregado"] = entregados
            data["no_entregado"] = no_entregados
            data["devolucion"] = devoluciones
            data["cantidad_registrada"] = cantidad_registrada
            data["cantidad_real"] = cantidad_real
            data["keys_productos"] = key_productos
            data["total_ventas"] = total_ventas
            data["total_compras"] = total_compras
            data["total_pedidos"] = total_pedidos
            data["total_devoluciones"] = total_devoluciones

        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data,safe=False)


@login_required(login_url='Login')
def consultData(request):
    data ={}
    if request.POST:
        try:
            data["productos"] = []
            id = int(request.POST["id"])
            productos = ProductosEgreso.objects.filter(egreso=id)
            for i in productos:
                item = i.toJSON()
                item["descripcion"] = i.producto.descripcion
                item["codigo"] = i.producto.codigo
                data["productos"].append(item)

        except Exception as e:
            data['error'] = str(e)      
    else:
        data['error'] = "Ha ocurrido un error"
       
    
    return JsonResponse(data,safe=False)

@login_required(login_url='Login')
def consultDatab(request):
    data ={}
    if request.POST:
        try:
            data["productos"] = []
            id = int(request.POST["id"])
            productos = ProductosEgreso.objects.filter(egreso=id)
            for i in productos:
                item = i.toJSON()
                item["descripcion"] = i.producto.descripcion
                item["codigo"] = i.producto.codigo
                data["productos"].append(item)

        except Exception as e:
            data['error'] = str(e)      
    else:
        data['error'] = "Ha ocurrido un error"
       
    
    return JsonResponse(data,safe=False)


@login_required(login_url='Login')
def consultDatai(request):
    data ={}
    if request.POST:
        try:
            data["productos"] = []
            id = int(request.POST["id"])
            productos_ingreso = ProductosIngreso.objects.filter(ingreso=id)
            print(id)
            for i in productos_ingreso:
                item = i.toJSON()
                item["descripcion"] = i.producto.descripcion
                item["codigo"] = i.producto.codigo
                data["productos"].append(item)
            
            print(data["productos"])

        except Exception as e:
            data['error'] = str(e)  
            print(data["error"])    
    else:
        data['error'] = "Ha ocurrido un error"
       
    
    return JsonResponse(data,safe=False)

@login_required(login_url='Login')
def proveedor_view(request):
    
    form_personal = ProveedorForm()
    form_editar_personal = EditarProveedorForm()
    personal = Proveedor.objects.all()
    num_personal = len(personal)

    context = {
        'form_personal': form_personal,
        'form_editar_personal': form_editar_personal,
        'personal': personal,
        'num_personal': num_personal
    }
    return render(request, 'proveedores.html', context)


@login_required(login_url='Login')
def add_proveedor_view(request):
    if request.POST:
        #print(request.POST)
        form = ProveedorForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages.warning(request,"Proveedor ya agregado o datos incorrectos")
                return redirect('Proveedor')


    return redirect('Proveedor')


@login_required(login_url='Login')
def edit_proveedor_view(request):
    if request.POST:
        producto = Proveedor.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarProveedorForm(
            request.POST, request.FILES, instance=producto)
        if form.is_valid:
            form.save()

    return redirect('Proveedor')


@login_required(login_url='Login')
def delete_proveedor_view(request):
    if request.POST:
        if int(request.POST.get('id_personal_eliminar')) == 1:
            messages.warning(request, "No es posible eliminar este proveedor")
            return redirect('Proveedor')
        personal = Proveedor.objects.get(pk=request.POST.get('id_personal_eliminar'))
        personal.delete()
        
    return redirect('Proveedor')


@login_required(login_url='Login')
def cliente_view(request):

    form_personal = ClienteForm()
    form_editar_personal = EditarClienteForm()
    personal = Cliente.objects.all()
    num_personal = len(personal)

    context = {
        'form_personal': form_personal,
        'form_editar_personal': form_editar_personal,
        'personal': personal,
        'num_personal': num_personal
    }
    return render(request, 'clientes.html', context)


@login_required(login_url='Login')
def add_cliente_view(request):
    if request.POST:
        #print(request.POST)
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages.warning(request,"Cliente ya agregado o datos incorrectos")
                return redirect('Cliente')


    return redirect('Cliente')


@login_required(login_url='Login')
def edit_cliente_view(request):
    if request.POST:
        producto = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarClienteForm(
            request.POST, request.FILES, instance=producto)
        if form.is_valid:
            form.save()

    return redirect('Cliente')


@login_required(login_url='Login')
def delete_cliente_view(request):
    if request.POST:
        if int(request.POST.get('id_personal_eliminar')) == 1:
            messages.warning(request, "No es posible eliminar este cliente")
            return redirect('Cliente')
        personal = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        personal.delete()
        
    return redirect('Cliente')


@login_required(login_url='Login')
def inventario_view(request):
    
    form_producto = ProductoForm()
    form_editar_producto = EditarProductoForm()
    form_ajustar = InventarioForm()
    productos = Producto.objects.all()
    num_productos = len(productos)
    empresa = Empresa.objects.get(pk=1)
    moneda = empresa.moneda

    context = {
        'form_producto': form_producto,
        'form_editar_producto': form_editar_producto,
        'productos': productos,
        'num_productos': num_productos, 
        'form_ajustar_producto': form_ajustar,
        'moneda': moneda
    }
    return render(request, 'inventario.html', context)


@login_required(login_url='Login')
def delete_producto_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
        if producto.imagen:
            os.remove(producto.imagen.path)
        producto.delete()
        
    return redirect('Product')


@login_required(login_url='Login')
def add_product_view(request):
    if request.POST:
        #print(request.POST)
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages.warning(request,"Producto ya agregado o datos incorrectos")
                return redirect('Product')


    return redirect('Product')


@login_required(login_url='Login')
def edit_product_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_editar'))
        form = EditarProductoForm(
            request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()

    return redirect('Product')

@login_required(login_url='Login')
def ajuste_product_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_ajustar'))
        form = InventarioForm(
            request.POST, request.FILES, instance=producto)
        if form.is_valid():
            ajuste = Ajuste(producto=producto, cantidad_registrada=float(request.POST["cantidadanterior"]),cantidad_real=float(request.POST["cantidad"]), fecha=HOY,responsable=request.user)
            form.save()
            ajuste.save()

    return redirect('Product')

class ventas(ListView):
    model = Egreso
    template_name = 'ventas.html'

    @method_decorator(login_required(login_url='Login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    """
    def get_queryset(self):
        return ProductosPreventivo.objects.filter(
            preventivo=self.kwargs['id']
        )
    """
    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)


    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        #context["preventivo"] = Preventivo.objects.get(pk=self.kwargs['id'])
        context["cliente"] = Cliente.objects.get(pk=1)
        context["productos_lista"] = Producto.objects.all()
        context["HOY"] = HOY
        context["clientes_lista"] = Cliente.objects.all()
        empresa = Empresa.objects.get(pk=1)
        moneda = empresa.moneda
        context["moneda"] = moneda
        try:
            context["last_id"] = int(Egreso.objects.latest('id').id) + 1
        except Exception as e:
            context["last_id"] = 1
        return context


class compras(ListView):
    model = Ingreso
    template_name = 'compras.html'

    @method_decorator(login_required(login_url='Login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    """
    def get_queryset(self):
        return ProductosPreventivo.objects.filter(
            preventivo=self.kwargs['id']
        )
    """
    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)


    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        #context["preventivo"] = Preventivo.objects.get(pk=self.kwargs['id'])
        context["cliente"] = Proveedor.objects.get(pk=1)
        context["productos_lista"] = Producto.objects.all()
        context["HOY"] = HOY
        context["clientes_lista"] = Proveedor.objects.all()
        context["moneda"] = Empresa.objects.get(pk=1).moneda
        context["form_responsable"] = ResponsableForm()
        try:
            context["last_id"] = int(Ingreso.objects.latest('id').id) + 1
        except Exception as e:
            context["last_id"] = 1
        return context


@login_required(login_url='Login')
def save_compra_view(request):
    if request.POST:
        data =[]
        try:
            action = request.POST['action']
            if action == "save":
                datos = json.loads(request.POST["verts"])
                id_cliente = request.POST["id_cliente"]
                codigo = request.POST["codigo"]
                comentarios = request.POST["comentarios"]
                estado = request.POST["estado"]
                cliente = Proveedor.objects.get(pk=id_cliente)
                subpiezas = float(datos["total"])
                fecha = request.POST["fecha"]

                venta = Ingreso(proveedor=cliente, fecha=fecha, subtotalpiezas=subpiezas, codigo=codigo, comentarios=comentarios, estado=estado)
                venta.save()

                for i in datos["products"]:
                    pr_save = Producto.objects.get(pk=float(i["id"]))
                    suma = float(pr_save.cantidad) + float(i["cantidad"])
                    pr_save.costo = float(i["precio"])
                    pr_save.cantidad = suma
                    pr_save.save()

                    product = ProductosIngreso(ingreso=venta, producto=pr_save,cantidad=float(i["cantidad"]),costo=float(i["precio"]),subtotal=float(i["subtotal"]))
                    product.save()
                
                messages.info(request,"Ingreso agregado con éxito")
        except Exception as e:
            data['error'] = str(e)

    return JsonResponse(data,safe=False)


@login_required(login_url='Login')
def export_pdf_view(request, id, iva):
    #print(id)
    template = get_template("ticket.html")
    #print(id)
    subtotal = 0 
    iva_suma = 0 

    venta = Egreso.objects.get(pk=float(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
    vendedor = Personal.objects.all()
        
    hora_actual = venta.updated.time()
    fecha_ficticia = venta.fecha_pedido
    # Combina la fecha ficticia con la hora actual
    fecha_hora_actual = datetime.combine(fecha_ficticia, hora_actual)

    Hora_entrega = fecha_hora_actual + timedelta(hours=1)
    total = venta.total
    A_cuenta = venta.pagado
    Saldo = total - A_cuenta
   
    

    




    
    

    for i in datos:
        subtotal = subtotal + float(i.subtotal)
        iva_suma = iva_suma + float(i.iva)

    empresa = Empresa.objects.get(pk=1)
    context ={
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'telefono': venta.cliente.telefono,
        'items': datos, 
        'total': total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
        
        'hora': venta.updated.time(),
        'Hora_entrega' : Hora_entrega,
        'A_cuenta' : A_cuenta,
        'Saldo' : Saldo,
        'vendedor' : vendedor,


    }
    html_template = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; ticket.pdf"
    css_url = os.path.join(settings.BASE_DIR,'index\static\index\css/bootstrap.min.css')
    #HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])
   
    font_config = FontConfiguration()
    HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target=response, font_config=font_config,stylesheets=[CSS(css_url)])

    return response

@login_required(login_url='Login')
def export_pdf_carta_view(request, id, iva):
    #print(id)
    template = get_template("pdf.html")
    #print(id)
    subtotal = 0 
    iva_suma = 0 

    venta = Egreso.objects.get(pk=float(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
 


    
    for i in datos:
        subtotal = subtotal + float(i.subtotal)
        iva_suma = iva_suma + float(i.iva)

    empresa = Empresa.objects.get(pk=1)
    context ={
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'items': datos, 
        'total': venta.total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
    

    }
    
    html_template = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; ticket.pdf"
    css_url = os.path.join(settings.BASE_DIR,'index\static\index\css/bootstrap.min.css')
    #HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])
   
    font_config = FontConfiguration()
    HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target=response, font_config=font_config,stylesheets=[CSS(css_url)])

    return response

@login_required(login_url='Login')
def delete_correctivo_view(request):
    if request.POST:
        correctivo = Egreso.objects.get(pk=request.POST.get('id_correctivo_eliminar'))
        correctivo.delete()
        
    return redirect('Index')

@login_required(login_url='Login')
def edit_correctivo_view(request):
    if request.POST:
        correctivo = Egreso.objects.get(pk=request.POST.get('id_correctivo_editar'))

    return redirect('Index')


@login_required(login_url='Login')
def delete_ingreso_view(request):
    if request.POST:
        correctivo = Ingreso.objects.get(pk=request.POST.get('id_correctivo_eliminar'))
        correctivo.delete()
        
    return redirect('Ingresos')

@login_required(login_url='Login')
def edit_ingreso_view(request):
    if request.POST:
        try:
            correctivo = Ingreso.objects.get(pk=request.POST.get('id_correctivo_editar'))
            print("Si entramos aqui")
            form = IngresoForm(
                request.POST, request.FILES, instance=correctivo)
            if form.is_valid():
                form.save()
        except error as e:
            print(e)


    return redirect('Ingresos')

@login_required(login_url='Login')
def save_venta_view(request):
    if request.POST:
        data =[]
        try:
            action = request.POST['action']
            if action == "save":
                datos = json.loads(request.POST["verts"])
                id_cliente = request.POST["id_cliente"]
                comentarios = request.POST["comentarios"]
                cliente = Cliente.objects.get(pk=id_cliente)
                total = float(datos["total"])
                fecha = request.POST["fecha"]
                ticket_num = float( request.POST["ticket"])
                efectivo = float( request.POST["efectivo"])
                tarjeta = float( request.POST["tarjeta"])
                transferencia = float( request.POST["transferencia"])
                vales = float( request.POST["vales"])
                otro = float( request.POST["otro"])
                pagado = efectivo + tarjeta + transferencia + vales + otro
                desglosar_num = float( request.POST["desglosar"])

                if ticket_num == 1:
                    ticket =True
                elif ticket_num == 0:
                    ticket = False
                
                if desglosar_num == 1:
                    desglosar =True
                elif desglosar_num == 0:
                    desglosar = False

                venta = Egreso(cliente=cliente, fecha_pedido=fecha, total=total, pagado=pagado, comentarios=comentarios, ticket=ticket, desglosar=desglosar)
                venta.save()

                metodo = MetodoPago(egreso=venta,efectivo=efectivo, tarjeta=tarjeta, transferencia=transferencia, vales=vales, otro=otro)
                metodo.save()

                data.append(venta.id)
                data.append(venta.ticket)
                data.append(venta.desglosar)

                for i in datos["products"]:
                    pr_save = Producto.objects.get(pk=float(i["id"]))

                    if pr_save.servicio == False:
                        porcion_convertida = float(i["cantidad"]) * (1/float(pr_save.porcion))
                        suma = float(pr_save.cantidad) - porcion_convertida
                        pr_save.cantidad = suma
                        pr_save.save()

                   
                    iva_producto = float(pr_save.iva)

                    if iva_producto != 0:
                        subtotal = float(i["subtotal"]) / (1+iva_producto)
                        iva = subtotal * iva_producto
                    else:
                        subtotal = float(i["subtotal"])
                        iva = 0

                    product = ProductosEgreso(egreso=venta, producto=pr_save,cantidad=float(i["cantidad"]),precio=float(i["precio"]),subtotal=subtotal,iva=iva,total=float(i["subtotal"]))
                    product.save()
                    print(i["subtotal"])

                messages.info(request,"Venta agregada con éxito")
        except Exception as e:
            data['error'] = str(e)

    return JsonResponse(data,safe=False)

@login_required(login_url='Login')
def updateEntregados(request):
    data ={}
    if request.POST:
        try:
            datos = json.loads(request.POST["productos"])
            for i in datos: 
                print(i["entregado"])
                registro = ProductosEgreso.objects.get(pk=int(i["id"]))
                registro.entregado = i["entregado"]
                registro.save()

        except Exception as e:
            data['error'] = str(e)      
    else:
        data['error'] = "Ha ocurrido un error"
       
    
    return JsonResponse(data,safe=False)


@login_required(login_url='Login')
def updateDevoluciones(request):
    data ={}
    if request.POST:
        try:
            datos = json.loads(request.POST["productos"])
            for i in datos: 
                print(i["devolucion"])
                registro = ProductosEgreso.objects.get(pk=int(i["id"]))
                registro.devolucion = i["devolucion"]
                if registro.devolucion == True:
                    registro.entregado = False
                registro.save()

        except Exception as e:
            data['error'] = str(e)      
    else:
        data['error'] = "Ha ocurrido un error"
       
    
    return JsonResponse(data,safe=False)

@login_required(login_url='Login')
def devoluciones_view(request):
    
    form_devolucion = DevolucionForm()
    devoluciones = Devolucion.objects.all()
    num_devoluciones = len(devoluciones)

    context = {
        'form_devolucion': form_devolucion,
        'devoluciones': devoluciones,
        'num_productos': num_devoluciones,
    }
    return render(request, 'devoluciones.html', context)

@login_required(login_url='Login')
def add_devolucion_view(request):
    if request.POST:
        #print(request.POST)
        form = DevolucionForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages.warning(request,"Datos incorrectos")
                return redirect('Devoluciones')


    return redirect('Devoluciones')

@login_required(login_url='Login')
def delete_devolucion_view(request):
    if request.POST:
        correctivo = Devolucion.objects.get(pk=request.POST.get('id_correctivo_eliminar'))
        correctivo.delete()
        
    return redirect('Devoluciones')

@login_required(login_url='Login')
def creditos_view(request):
    form_add = PagosEgresoForm()
    creditos = Egreso.objects.filter(Q(total__gt=F('pagado')))
    historial = PagosEgreso.objects.all()
    moneda = Empresa.objects.get(pk=1).moneda


    context = {
        'form_add': form_add,
        'creditos': creditos,     
        'historial': historial,
        'moneda': moneda
    }
    return render(request, 'creditos.html', context)

@login_required(login_url='Login')
def add_abono_view(request):
    if request.POST:
        fecha = request.POST["fecha"]
        monto = float(request.POST["monto"])
        comentarios = request.POST["comentarios"]
        venta = Egreso.objects.get(pk=request.POST.get('id_personal_editar'))
        
        venta.pagado = float(venta.pagado) + monto
        venta.save()

        abono = PagosEgreso(egreso=venta,fecha=fecha,monto=monto, comentarios=comentarios)
        abono.save()


    return redirect('Creditos')


