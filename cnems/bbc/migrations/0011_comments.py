# Generated by Django 2.1.2 on 2018-12-04 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbc', '0010_remove_likes_sum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_center', models.CharField(max_length=200)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbc.News')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbc.Users')),
            ],
        ),
    ]
