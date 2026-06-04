from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0011_alter_logro_condicion_prediccionerror_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ejercicio',
            name='tema',
            field=models.CharField(max_length=100, blank=True, help_text='Ej: tabla_11, tabla_8, suma_fracciones, division_decimales'),
        ),
        migrations.AddField(
            model_name='ejercicio',
            name='subtema',
            field=models.CharField(max_length=100, blank=True, help_text='Ej: multiplicacion, fracciones, division'),
        ),
        migrations.CreateModel(
            name='AnalisisErrorTema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(max_length=100)),
                ('subtema', models.CharField(max_length=100)),
                ('cantidad_errores', models.IntegerField(default=0)),
                ('cantidad_aciertos', models.IntegerField(default=0)),
                ('tiempo_promedio_ms', models.IntegerField(default=0)),
                ('fecha_analisis', models.DateTimeField(auto_now=True)),
                ('nino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analisis_temas', to='tareas.nino')),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analisis_temas', to='tareas.tarea')),
            ],
            options={
                'unique_together': {('nino', 'tarea', 'tema')},
            },
        ),
    ]
