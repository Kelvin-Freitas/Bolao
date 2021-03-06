# Generated by Django 2.2.16 on 2020-10-24 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0016_auto_20201023_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='iconTimeCasa',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='iconTimeVisitante',
        ),
        migrations.AlterField(
            model_name='apostas',
            name='aposta_vencedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bolao.Time'),
        ),
        migrations.AlterField(
            model_name='partida',
            name='timeCasa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partida_timecasa', to='bolao.Time'),
        ),
        migrations.AlterField(
            model_name='partida',
            name='timeVisitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partida_timevisitante', to='bolao.Time'),
        ),
        migrations.AlterField(
            model_name='resultado',
            name='vencedorPartida',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bolao.Time'),
        ),
    ]
