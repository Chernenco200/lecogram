# Generated by Django 3.2.9 on 2022-06-11 18:46

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20220511_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='imagen',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, size=[100, 100], upload_to='empresa'),
        ),
    ]
