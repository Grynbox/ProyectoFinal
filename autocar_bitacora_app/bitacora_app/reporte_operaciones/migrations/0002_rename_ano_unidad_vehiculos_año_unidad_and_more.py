# Generated by Django 5.0.8 on 2024-09-23 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_operaciones', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiculos',
            old_name='ano_unidad',
            new_name='año_unidad',
        ),
        migrations.AlterField(
            model_name='mecanico',
            name='especialidad_mecanico',
            field=models.CharField(choices=[('CARROCERIA', 'Carroceria'), ('ELECTRICO', 'Electrico'), ('PINTURA', 'Pintura')], max_length=25),
        ),
        migrations.AlterField(
            model_name='reportereparacion',
            name='tipo_ingreso',
            field=models.CharField(choices=[('CORRECTIVO', 'Correctivo'), ('RESCATE', 'Rescate'), ('PREVENTIVO', 'Preventivo'), ('ACCIDENTE', 'Accidente')], max_length=20),
        ),
        migrations.AlterField(
            model_name='usuarioautocar',
            name='departamento',
            field=models.CharField(choices=[('OPERACIONES', 'Operaciones'), ('TALLER', 'Taller'), ('ALMACEN', 'Almacen'), ('REPARACION', 'Mecanico')], max_length=20),
        ),
        migrations.AlterField(
            model_name='vehiculos',
            name='zona_unidad',
            field=models.CharField(choices=[('NORTE', 'Norte'), ('SUR', 'Sur'), ('CENTRO', 'Centro'), ('HOTELES', 'Hoteles')], max_length=20),
        ),
    ]
