# Generated by Django 5.0.8 on 2024-10-30 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_operaciones', '0006_rename_reparacion_reportemecanico_reparacion_selecionadas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportemecanico',
            old_name='reparacion_selecionadas',
            new_name='reparacion_selecionada',
        ),
    ]
