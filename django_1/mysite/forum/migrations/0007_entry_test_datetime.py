# Generated by Django 2.1.2 on 2018-10-27 06:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20181027_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='test_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]