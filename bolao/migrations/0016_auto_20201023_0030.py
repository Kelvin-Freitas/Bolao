# Generated by Django 2.2.16 on 2020-10-23 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0015_auto_20201021_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apostas',
            name='partida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bolao.Partida'),
        ),
        migrations.AlterField(
            model_name='partida',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='resultado',
            name='partida',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bolao.Partida'),
        ),
    ]
