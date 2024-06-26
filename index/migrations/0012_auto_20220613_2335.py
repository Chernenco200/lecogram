# Generated by Django 3.2.9 on 2022-06-14 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_producto_barcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='egreso',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='egreso',
            name='destino',
        ),
        migrations.RemoveField(
            model_name='egreso',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='egreso',
            name='fecha_cierre',
        ),
        migrations.RemoveField(
            model_name='egreso',
            name='file',
        ),
        migrations.RemoveField(
            model_name='egreso',
            name='responsable',
        ),
        migrations.RemoveField(
            model_name='egreso',
            name='subtotalpiezas',
        ),
        migrations.RemoveField(
            model_name='egreso',
            name='traspaso',
        ),
        migrations.AddField(
            model_name='egreso',
            name='iva',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='egreso',
            name='pagado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='egreso',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='egreso',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.CreateModel(
            name='PagosEgreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(max_length=255)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('egreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.egreso')),
            ],
            options={
                'verbose_name': 'pagos egreso',
                'verbose_name_plural': 'pagos egreso',
                'order_with_respect_to': 'created',
            },
        ),
    ]
