# Generated by Django 4.2.3 on 2023-10-27 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coach',
            name='image',
        ),
    ]
