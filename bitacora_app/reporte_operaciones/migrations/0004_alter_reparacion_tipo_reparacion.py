# Generated by Django 5.0.8 on 2024-10-30 04:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_operaciones', '0003_rename_fallo_reparacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reparacion',
            name='tipo_reparacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporte_operaciones.tiporeparacion'),
        ),
    ]
