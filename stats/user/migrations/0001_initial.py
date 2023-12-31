# Generated by Django 4.2.3 on 2023-11-29 20:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import user.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username can only contain lowercase letters, numbers, and underscores.', regex='^[a-z0-9_]+$')], verbose_name='username')),
                ('phone_number', models.CharField(max_length=30, unique=True, verbose_name='phone_number')),
                ('image', models.ImageField(blank=True, null=True, upload_to=user.models.image_directory_path)),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first_name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last_name')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(blank=True, choices=[('admin', 'ADMIN'), ('coach', 'COACH'), ('organizator', 'ORGANIZATOR'), ('president', 'PRESIDENT')], max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=8)),
                ('phone_number', models.CharField(max_length=20)),
                ('token_type', models.CharField(choices=[('password_reset', 'PASSWORD_RESET')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
