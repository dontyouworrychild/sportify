# Generated by Django 4.2.3 on 2023-11-18 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
            ],
        ),
    ]
