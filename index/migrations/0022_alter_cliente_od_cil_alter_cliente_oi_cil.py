# Generated by Django 4.0.5 on 2024-07-05 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0021_alter_cliente_od_cil_alter_cliente_oi_cil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='OD_Cil',
            field=models.CharField(blank=True, default='0 X 0°', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='OI_Cil',
            field=models.CharField(blank=True, default='0 X 0°', max_length=10, null=True),
        ),
    ]
