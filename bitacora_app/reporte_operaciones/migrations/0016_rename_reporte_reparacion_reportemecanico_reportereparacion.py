# Generated by Django 5.0.8 on 2024-11-05 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_operaciones', '0015_alter_reportemecanico_hora_inicio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportemecanico',
            old_name='reporte_reparacion',
            new_name='reporteReparacion',
        ),
    ]
