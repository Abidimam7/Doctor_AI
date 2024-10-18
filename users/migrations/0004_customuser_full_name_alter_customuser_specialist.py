# Generated by Django 4.2.16 on 2024-10-14 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_medical_license_customuser_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='specialist',
            field=models.CharField(blank=True, choices=[('Cardiologist', 'Cardiologist'), ('Dermatologist', 'Dermatologist'), ('Pediatrician', 'Pediatrician'), ('Surgeon', 'Surgeon'), ('General Physician', 'General Physician')], max_length=100, null=True),
        ),
    ]
