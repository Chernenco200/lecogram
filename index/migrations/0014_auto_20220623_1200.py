# Generated by Django 3.2.9 on 2022-06-23 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0013_auto_20220614_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='egreso',
            name='iva',
        ),
        migrations.RemoveField(
            model_name='egreso',
            name='subtotal',
        ),
        migrations.AlterField(
            model_name='productosegreso',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='productosegreso',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='productosegreso',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.CreateModel(
            name='MetodoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('efectivo', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('tarjeta', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('transferencia', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('vales', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('otro', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('egreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.egreso')),
            ],
            options={
                'verbose_name': 'metodo pago',
                'verbose_name_plural': 'metodos pago',
            },
        ),
    ]