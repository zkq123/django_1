# Generated by Django 2.1.2 on 2018-10-24 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('full', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='bar',
            index=models.Index(fields=['price', 'pub_date'], name='price_pub_date_idx'),
        ),
    ]
