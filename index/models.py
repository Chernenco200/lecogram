
from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django_resized import ResizedImageField


TODAY = date.today()
# Create your models here.

ESTADOS = ( 
    ("Programado", "Programado"), 
    ("En espera", "En espera"), 
    ("En proceso", "En proceso"), 
    ("Atrasado", "Atrasado"),  
    ("Realizado", "Realizado")
    )

UNIDAD_COMPRA = ( 
    ("Pieza", "Pieza"),  
    ("Kg", "Kg"), 
    ("gramos", "gramos"),
    ("Lt", "Lt"), 
    ("Metro", "Metro"),  
    ("Caja", "Caja"), 
    ("Onza", "Onza"),
    ("Charola", "Charola"),
    ("Otro", "Otro")
    )

def validate_image(imagen):
    max_height = 100
    max_width = 100
    height = imagen.height 
    width = imagen.width
    if width > max_width or height > max_height:
        raise ValidationError("El largo de la imagen no debe superar los {} px y ancho de la imagen no deben superar los {} px".format(max_height, max_width))


def validate_image_equipo(imagen):
    max_height = 300
    max_width = 400
    height = imagen.height 
    width = imagen.width
    if width > max_width or height > max_height:
        raise ValidationError("El largo de la imagen no debe superar los {} px y ancho de la imagen no deben superar los {} px".format(max_height, max_width))


class Iva (models.Model):
    monto = models.DecimalField(max_digits=15, decimal_places=2, null=False)

    class Meta:
        verbose_name='iva'
        verbose_name_plural = 'iva'
    
    def __str__(self):
        return str(self.monto)

class Almacen (models.Model):
    codigo = models.CharField(max_length=255, unique=True, null=True, blank = True)
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='almacen', null=True, blank=True)

    class Meta:
        verbose_name='almacen'
        verbose_name_plural = 'almacenes'
    
    def __str__(self):
        return self.nombre

class Area (models.Model):
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=255, unique=True, null=True, blank = True)
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='area', null=True, blank=True)

    class Meta:
        verbose_name='area'
        verbose_name_plural = 'areas'
    
    def __str__(self):
        return self.nombre


class Proveedor (models.Model):
    codigo = models.CharField(max_length=255, null=True, blank = True)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(upload_to='proveedor', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='proveedor'
        verbose_name_plural = 'proveedores'
    
    def __str__(self):
        return self.nombre

class Cliente (models.Model):
    codigo = models.CharField(max_length=255, null=True, blank = True)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(upload_to='cliente', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='cliente'
        verbose_name_plural = 'clientes'
    
    def __str__(self):
        return self.nombre

class Personal (models.Model):
    codigo = models.CharField(max_length=255, unique=True, null=True, blank = True)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, null=True)
    cargo = models.CharField(max_length=255, null=True)
    imagen = models.ImageField(upload_to='personal', null=True, blank=True)
    zona = models.ForeignKey(Area, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='tecnico'
        verbose_name_plural = 'tecnicos'
    
    def __str__(self):
        return self.nombre

class Producto (models.Model):
    codigo = models.CharField(max_length=255, null=True, blank = True)
    descripcion =  models.CharField(max_length=255, unique=True, null=False)
    imagen = ResizedImageField(size=[100, 100], upload_to='productos', blank=True, null=True)
    costo = models.DecimalField(max_digits=20, decimal_places=2, null=False, default = 0)
    precio = models.DecimalField(max_digits=20, decimal_places=2, null=False, default =0)
    iva = models.DecimalField(max_digits=20, decimal_places=2, null=False, default =0)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2 , null=False,default=0)
    porcion = models.DecimalField(max_digits=20, decimal_places=2 , null=False,default=1)
    unidad = models.CharField(max_length=255, choices = UNIDAD_COMPRA, default='Pieza', null=False)
    unidad_venta = models.CharField(max_length=255, choices = UNIDAD_COMPRA, default='Pieza', null=False)
    servicio = models.BooleanField(default=False)
    barcode = models.CharField(max_length=255, unique=False, null=True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='producto'
        verbose_name_plural = 'productos'
        order_with_respect_to = 'descripcion'
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self, exclude=['imagen', 'created', 'updated'])
        return item



class Ingreso (models.Model):
    fecha = models.DateField(max_length=255)
    codigo = models.CharField(max_length=255, unique=True, null=True, blank = True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL , null=True , related_name='proveedori')
    subtotalpiezas = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    estado = models.CharField(max_length=255, choices = ESTADOS, default='Realizado', null=False)
    file = models.FileField(null=True, upload_to='ingresos', blank=True)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)

    class Meta:
        verbose_name='ingreso'
        verbose_name_plural = 'ingresos'
        order_with_respect_to = 'fecha'
    
    def __str__(self):
        return str(self.id)

class ProductosIngreso(models.Model):
    ingreso = models.ForeignKey(Ingreso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2 , null=False)
    costo = models.DecimalField(max_digits=15, decimal_places=2 , null=False , default=0)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2 , null=False , default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='producto ingreso'
        verbose_name_plural = 'productos ingreso'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.producto
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['created'])
        return item


class Egreso(models.Model):
    fecha_pedido = models.DateField(max_length=255)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL , null=True , related_name='clientee')
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pagado = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    ticket = models.BooleanField(default=True)
    desglosar = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)

    class Meta:
        verbose_name='egreso'
        verbose_name_plural = 'egresos'
        order_with_respect_to = 'fecha_pedido'
    
    def __str__(self):
        return str(self.id)
   
class MetodoPago(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    efectivo = models.DecimalField(max_digits=20, decimal_places=2 , default=0)
    tarjeta = models.DecimalField(max_digits=20, decimal_places=2 , default=0)
    transferencia = models.DecimalField(max_digits=20, decimal_places=2 , default=0)
    vales = models.DecimalField(max_digits=20, decimal_places=2 , default=0)
    otro = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name='metodo pago'
        verbose_name_plural = 'metodos pago'
    
    def __str__(self):
        return str(self.id)

class ProductosEgreso(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2 , null=False)
    precio = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    iva = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    created = models.DateTimeField(auto_now_add=True)
    entregado = models.BooleanField(default=True)
    devolucion = models.BooleanField(default=False)

    class Meta:
        verbose_name='producto egreso'
        verbose_name_plural = 'productos egreso'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.producto
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['created'])
        return item

class PagosEgreso(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    fecha = models.DateField(max_length=255)
    monto = models.DecimalField(max_digits=20, decimal_places=2 , null=False)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='pagos egreso'
        verbose_name_plural = 'pagos egreso'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.monto
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['created'])
        return item

class Devolucion(models.Model):
    fecha = models.DateField(max_length=255)
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=255, unique=True, null=True, blank = True)
    subtotalpiezas = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)

    class Meta:
        verbose_name='devolucion'
        verbose_name_plural = 'devoluciones'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.created


class Ajuste(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    cantidad_registrada = models.DecimalField(max_digits=15, decimal_places=2 , null=False, default=0)
    cantidad_real = models.DecimalField(max_digits=15, decimal_places=2 , null=False, default=0)
    fecha = models.DateField(max_length=255)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsablea')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)

    class Meta:
        verbose_name='ajuste'
        verbose_name_plural = 'ajustes'
    
    def __str__(self):
        return str(self.id)


class Empresa (models.Model):
    nombre = models.CharField(max_length=255)
    domicilio = models.CharField(max_length=255, null=True)
    telefono = models.CharField(max_length=255, null=True)
    imagen = ResizedImageField(size=[100, 100], upload_to='empresa', blank=True, null=True)
    moneda = models.CharField(max_length=255, null=False, blank=False, default="$" )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='empresa'
        verbose_name_plural = 'empresa'
    
    def __str__(self):
        return self.nombre