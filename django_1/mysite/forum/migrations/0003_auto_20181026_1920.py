# Generated by Django 2.1.2 on 2018-10-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
