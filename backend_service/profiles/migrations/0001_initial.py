# Generated by Django 5.1.3 on 2024-12-04 09:13

import django.db.models.deletion
import profiles.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='Username')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='Location')),
                ('total_bookings', models.BigIntegerField(default=0, verbose_name='Total Bookings')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=profiles.models.profile_picture_upload_path, verbose_name='Profile Picture')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
