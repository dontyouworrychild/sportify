# Generated by Django 4.2.3 on 2023-11-05 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='blue_corner_winner',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='game',
            name='red_corner_winner',
            field=models.BooleanField(default=True),
        ),
    ]