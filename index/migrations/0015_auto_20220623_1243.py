# Generated by Django 3.2.9 on 2022-06-23 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0014_auto_20220623_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='unidad_venta',
            field=models.CharField(choices=[('Pieza', 'Pieza'), ('Kg', 'Kg'), ('gramos', 'gramos'), ('Lt', 'Lt'), ('Metro', 'Metro'), ('Caja', 'Caja'), ('Onza', 'Onza'), ('Charola', 'Charola'), ('Otro', 'Otro')], default='Pieza', max_length=255),
        ),
        migrations.AlterField(
            model_name='producto',
            name='unidad',
            field=models.CharField(choices=[('Pieza', 'Pieza'), ('Kg', 'Kg'), ('gramos', 'gramos'), ('Lt', 'Lt'), ('Metro', 'Metro'), ('Caja', 'Caja'), ('Onza', 'Onza'), ('Charola', 'Charola'), ('Otro', 'Otro')], default='Pieza', max_length=255),
        ),
    ]
