# Generated by Django 3.2.9 on 2022-06-11 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20220611_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='barcode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
