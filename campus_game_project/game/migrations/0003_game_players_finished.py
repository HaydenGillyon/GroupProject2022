# Generated by Django 4.0.2 on 2022-03-02 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_game_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='players_finished',
            field=models.IntegerField(default=0),
        ),
    ]
