# Generated by Django 4.2.3 on 2023-11-05 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_game_blue_corner_winner_game_red_corner_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='blue_corner_winner',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='red_corner_winner',
            field=models.BooleanField(default=False),
        ),
    ]