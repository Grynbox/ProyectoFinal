# Generated by Django 5.0.8 on 2024-10-31 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporte_operaciones', '0011_alter_reportereparacion_id_reporte_mecanico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportereparacion',
            name='id_reporte_mecanico',
        ),
        migrations.AddField(
            model_name='reportereparacion',
            name='id_reporte_mecanico',
            field=models.ManyToManyField(blank=True, null=True, to='reporte_operaciones.reportemecanico'),
        ),
    ]