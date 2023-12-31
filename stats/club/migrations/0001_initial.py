# Generated by Django 4.2.3 on 2023-11-29 20:25

import club.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('logo', models.ImageField(blank=True, upload_to=club.models.logo_directory_path)),
                ('location', models.CharField(max_length=50, verbose_name='location')),
            ],
            options={
                'verbose_name': 'club',
                'verbose_name_plural': 'clubs',
            },
        ),
    ]
