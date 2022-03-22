# Generated by Django 4.0.1 on 2022-03-21 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('welcome', '0001_initial'),
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
                ('hiding_time', models.IntegerField(default=60)),
                ('seeking_time', models.IntegerField(default=600)),
                ('seeker_num', models.IntegerField(default=1)),
                ('radius', models.IntegerField(default=100)),
                ('lobby_longitude', models.FloatField(default=0.0)),
                ('lobby_latitude', models.FloatField(default=0.0)),
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
                ('user', models.ForeignKey(
                    default=None, on_delete=django.db.models.deletion.CASCADE, to='welcome.user')),
            ],
        ),
    ]
