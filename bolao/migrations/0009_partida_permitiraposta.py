# Generated by Django 2.2.16 on 2020-10-20 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0008_partida_rodada'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='permitirAposta',
            field=models.BooleanField(default=True),
        ),
    ]