# Generated by Django 4.2.16 on 2024-10-14 11:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diagnosis', '0007_appointment_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('doctor', 'patient', 'date', 'time')},
        ),
    ]
