# Generated by Django 5.0.8 on 2024-10-31 01:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_operaciones', '0009_rename_nombre_reparacion_reparacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportereparacion',
            name='id_reporte_mecanico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportes_mecanicos', to='reporte_operaciones.reportemecanico'),
        ),
    ]
