# Generated by Django 3.2 on 2024-11-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoDiseñoApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrarusuario',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='registrarusuario',
            name='contrasena',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='registrarusuario',
            name='correo_electronico',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='registrarusuario',
            name='segundo_apellido',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='registrarusuario',
            name='segundo_nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
