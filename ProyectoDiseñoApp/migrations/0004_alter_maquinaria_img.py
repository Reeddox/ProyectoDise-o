# Generated by Django 3.2 on 2024-11-19 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoDiseñoApp', '0003_delete_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maquinaria',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='maquinarias/'),
        ),
    ]
