# Generated by Django 5.2.4 on 2025-07-13 10:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='ad',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
