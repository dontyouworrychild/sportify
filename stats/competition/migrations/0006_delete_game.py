# Generated by Django 4.2.3 on 2023-10-20 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0005_alter_game_blue_corner_alter_game_red_corner_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Game',
        ),
    ]
