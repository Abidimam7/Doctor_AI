# Generated by Django 4.2.16 on 2024-10-12 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrePrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_text', models.TextField(help_text='Act as a Senior Doctor Cunsultatnt', verbose_name='Pre-Prompt')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
