# Generated by Django 4.0.2 on 2022-03-02 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    # Updates the game models after a game is won
    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.CharField(default='N', max_length=20),
        ),
    ]
