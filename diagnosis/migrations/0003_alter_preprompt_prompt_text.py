# Generated by Django 4.2.16 on 2024-10-14 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0002_preprompt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preprompt',
            name='prompt_text',
            field=models.TextField(help_text='Enter the pre-prompt for AI responses', verbose_name='Pre-Prompt'),
        ),
    ]
