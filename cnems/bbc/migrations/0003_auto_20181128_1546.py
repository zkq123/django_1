# Generated by Django 2.1.2 on 2018-11-28 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbc', '0002_auto_20181127_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pays',
            name='pays_money',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]