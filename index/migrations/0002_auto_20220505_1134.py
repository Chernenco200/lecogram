# Generated by Django 3.2.9 on 2022-05-05 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='zona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.area'),
        ),
        migrations.AlterField(
            model_name='personal',
            name='zona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.area'),
        ),
        migrations.AlterField(
            model_name='traspaso',
            name='destino',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destinot', to='index.area'),
        ),
        migrations.AlterField(
            model_name='traspaso',
            name='procedencia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='procedenciat', to='index.area'),
        ),
        migrations.DeleteModel(
            name='Zona',
        ),
    ]
