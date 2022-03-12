# Generated by Django 4.0.1 on 2022-03-12 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lobby_code', models.IntegerField()),
                ('player_num', models.IntegerField()),
                ('players_finished', models.IntegerField(default=0)),
                ('game_start_time', models.FloatField(default=0)),
                ('running', models.BooleanField(default=False)),
                ('winner', models.CharField(default='N', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('seeker', models.BooleanField()),
                ('ready', models.BooleanField()),
                ('hider_code', models.CharField(max_length=4, null=True)),
                ('found', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
    ]
