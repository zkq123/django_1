# Generated by Django 2.1.2 on 2018-10-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20181026_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
