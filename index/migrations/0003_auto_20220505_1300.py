# Generated by Django 3.2.9 on 2022-05-05 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20220505_1134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productostraspaso',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='productostraspaso',
            name='traspaso',
        ),
        migrations.RemoveField(
            model_name='traspaso',
            name='destino',
        ),
        migrations.RemoveField(
            model_name='traspaso',
            name='procedencia',
        ),
        migrations.RemoveField(
            model_name='traspaso',
            name='responsable',
        ),
        migrations.AddField(
            model_name='producto',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='producto',
            name='zona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.area'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productosajuste',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.producto'),
        ),
        migrations.AlterField(
            model_name='productosdevolucion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.producto'),
        ),
        migrations.AlterField(
            model_name='productosegreso',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.producto'),
        ),
        migrations.AlterField(
            model_name='productosingreso',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.producto'),
        ),
        migrations.DeleteModel(
            name='Inventario',
        ),
        migrations.DeleteModel(
            name='ProductosTraspaso',
        ),
        migrations.DeleteModel(
            name='Traspaso',
        ),
    ]
