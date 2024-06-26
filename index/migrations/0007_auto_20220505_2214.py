# Generated by Django 3.2.9 on 2022-05-06 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_auto_20220505_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='productosegreso',
            name='entregado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='codigo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='codigo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
