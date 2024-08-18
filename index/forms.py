
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from index.models import Proveedor, Cliente,Producto, Personal, Empresa,Ingreso, Devolucion, PagosEgreso
from datetime import date

moneda = Empresa.objects.get(pk=1).moneda
TODAY = date.today()

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'id': 'usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')
    
    
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("El usuario o contraseña son incorrectos")


class ProveedorForm(forms.ModelForm):
    class Meta:
        imagen = forms.ImageField()
        model = Proveedor
        fields = ('codigo','nombre', 'telefono', 'imagen')
        labels = {
            'codigo': 'Código: ',
            'telefono': 'Telefono: ',
            'imagen': 'Imagen: ',
            'nombre': 'Descripcion: '
        }

class PagosEgresoForm(forms.ModelForm):
    
    class Meta:
        model = PagosEgreso
        fields = ('fecha','monto','comentarios')
        labels = {
            'fecha': 'Fecha: ',
            'monto': f'Monto {moneda} : ',
            'comentarios': 'Comentarios: '
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date' , 'value': TODAY }),
        }

class EditarProveedorForm(forms.ModelForm):

    class Meta:
        imagen = forms.ImageField()
        model = Proveedor
        fields = ('codigo','nombre', 'telefono', 'imagen')
        labels = {
            'codigo': 'Código: ',
            'telefono': 'Telefono: ',
            'imagen': 'Imagen: ',
            'nombre': 'Descripcion: '
        }

        widgets = {
            'codigo': forms.TextInput(attrs={'type': 'text', 'id': 'codigo_editar'}),
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono_editar'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        imagen = forms.ImageField()
        model = Cliente
        fields = ('codigo','nombre', 'Edad','telefono', 'OD_Esf','OI_Esf','OD_Cil','OI_Cil','ADD','DIP', 'imagen')
        labels = {
            'codigo': 'DNI: ',
            'nombre': 'Nombre: ',
            'Edad': 'Edad',
            'telefono': 'Telefono: ',
            'OD_Esf': 'OD_Esf',
            'OI_Esf': 'OI_Esf',
            'OD_Cil': 'OD_Cil',
            'OI_Cil': 'OI_Cil',
            'ADD': 'ADD',
            'DIP': 'DIP',
            'imagen': 'Imagen: ',
        }

class EditarClienteForm(forms.ModelForm):

    class Meta:
        imagen = forms.ImageField()
        model = Cliente
        fields = ('codigo','nombre','Edad','telefono','OD_Esf','OI_Esf','OD_Cil','OI_Cil','ADD','DIP', 'imagen')
        labels = {
            'codigo': 'DNI: ',
            'nombre': 'Nombre: ',
            'Edad': 'Edad: ',
            'telefono': 'Telefono: ',
            'OD_Esf': 'OD_Esf: ',
            'OI_Esf': 'OI_Esf: ',
            'OD_Cil': 'OD_Cil: ',
            'OI_Cil': 'OI_Cil: ',
            'ADD': 'ADD: ',
            'DIP': 'DIP: ',
            'imagen': 'Imagen: ',
            
        }

        widgets = {
            'codigo': forms.TextInput(attrs={'type': 'text', 'id': 'codigo_editar'}),
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'Edad': forms.TextInput(attrs={'id': 'Edad_editar'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono_editar'}),
            'OD_Esf': forms.TextInput(attrs={'id': 'OD_Esf_editar'}),
            'OI_Esf': forms.TextInput(attrs={'id': 'OI_Esf_editar'}),
            'OD_Cil': forms.TextInput(attrs={'id': 'OD_Cil_editar'}),
            'OI_Cil': forms.TextInput(attrs={'id': 'OI_Cil_editar'}),            
            'ADD': forms.TextInput(attrs={'id': 'ADD_editar'}),
            'DIP': forms.TextInput(attrs={'id': 'DIP_editar'}),


        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('cantidad',)
        labels = {
            'cantidad': 'Cantidad real: '
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        imagen = forms.ImageField()
        model = Producto
        fields = ('codigo','descripcion', 'imagen', 'costo','iva', 'precio', 'cantidad',  'unidad', 'porcion', 'unidad_venta' ,'servicio', 'barcode')
        labels = {
            'codigo': 'Código interno:',
            'descripcion': 'Descripción: ',
            'imagen': 'Imagen: ',
            'costo': 'Costo: ',
            'iva': 'IVA %: ',
            'precio': 'Precio unit. : ',
            'cantidad': 'Cantidad: ',
            'barcode': 'Código de barras: ',
            'servicio': ' ¿Es servicio?: ', 
            'porcion': 'Relación unidad venta por unidad de compra: (Ejemp. 24 x 1, 1 x 1) ',
            'unidad_venta': 'Unidad venta: '
        }
    
class EditarProductoForm(forms.ModelForm):

    class Meta:
        imagen = forms.ImageField()
        model = Producto
        fields = ('codigo', 'descripcion', 'imagen','costo','iva', 'unidad', 'precio', 'porcion', 'unidad_venta' ,'servicio','barcode')
        labels = {
            'codigo': 'Código:',
            'descripcion': 'Descripción: ',
            'imagen': 'Imagen: ',
            'costo': 'Costo: ',
            'iva': 'IVA %: ',
            'precio': 'Precio unit. : ',
            'barcode': 'Código de barras: ',
            'servicio': ' ¿Es servicio?: ', 
            'porcion': 'Relación unidad venta por unidad de compra: (Ejemp. 24 x 1, 1 x 1) ',
            'unidad_venta': 'Unidad venta: '
        }

        widgets = {
            'codigo': forms.TextInput(attrs={'id': 'codigo_editar'}),
            'descripcion': forms.TextInput(attrs={'id': 'descripcion_editar'}),
            'costo': forms.NumberInput(attrs={'id': 'costo_editar'}),
            'iva': forms.NumberInput(attrs={'id': 'iva_editar'}),
            'precio': forms.NumberInput(attrs={'id': 'precio_editar'}),
            'unidad': forms.Select(attrs={'id': 'unidad_editar'}),
            'porcion': forms.NumberInput(attrs={'id': 'porcion_editar'}),
            'barcode': forms.TextInput(attrs={'id': 'barcode_editar'}),
            'servicio': forms.CheckboxInput(attrs={'id': 'servicio_editar'}),
            'unidad_venta': forms.Select(attrs={'id': 'unidad_venta_editar'}),
        }



class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ('fecha', 'codigo','estado', 'file')
        labels = {
            'fecha': 'Fecha: ',
            'codigo': 'Código: ', 
            'estado': 'Estado: ',
            'file': 'Comprobante (*PDF,JPG,XLM): ', 

        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date','id': 'fecha_editar'}),
            'estado': forms.Select(attrs={'id': 'estado_editar'}),
            'codigo': forms.TextInput(attrs={'type': 'text', 'id': 'codigo_editar'}),
        }


class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Devolucion
        fields=('fecha', 'codigo', 'egreso', 'comentarios')
        labels = {
            'fecha': 'Fecha: ',
            'codigo': 'Código interno: ',
            'egreso': 'Venta: '

        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date' , 'value': TODAY }),
            'comentarios': forms.Textarea(attrs={'rows': '3'}),
        }


class PersonalForm(forms.ModelForm):
    class Meta:
        imagen = forms.ImageField()
        model = Personal
        fields = ('codigo','nombre','telefono', 'cargo', 'zona', 'imagen')
        labels = {
            'nombre': 'Nombre:',
            'telefono': 'Telefono: ',
            'cargo': 'Cargo: ', 
            'imagen': 'Imagen: ',
            'zona': 'Zona: ',
        }
        
class ResponsableForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ('codigo','estado','comentarios')
        labels = {
            'codigo': 'Código interno:',
            'estado': 'Estado de la compra: ',
            'comentarios': 'Comentarios: '
        }
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': '3'}),
        }

class EditarPersonalForm(forms.ModelForm):

    class Meta:
        imagen = forms.ImageField()
        model = Personal
        fields = ('nombre','telefono', 'cargo', 'zona', 'imagen', 'codigo')
        labels = {
            'nombre': 'Nombre:',
            'telefono': 'Telefono: ',
            'cargo': 'Cargo: ', 
            'imagen': 'Imagen: ',
            'zona': 'Zona: ',
            'codigo': 'DNI: ',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'id': 'nombre_editar'}),
            'telefono': forms.TextInput(attrs={'id': 'telefono_editar'}),
            'cargo': forms.TextInput(attrs={'id': 'cargo_editar'}),
            'zona': forms.Select(attrs={'id': 'zona_editar'}),
            'codigo': forms.TextInput(attrs={'id': 'codigo_editar'}),
        }

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ('nombre','domicilio', 'telefono', 'imagen', 'moneda')
        labels = {
            'nombre': 'Nombre:',
            'telefono': 'Contacto: ',
            'domicilio': 'Domicilio: ', 
            'imagen': 'Imagen: ',
            'moneda': 'Moneda: '
        }



