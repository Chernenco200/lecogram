# Generated by Django 3.2.9 on 2022-05-05 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20220505_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productosegreso',
            old_name='costo',
            new_name='precio',
        ),
        migrations.AlterField(
            model_name='egreso',
            name='codigo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]