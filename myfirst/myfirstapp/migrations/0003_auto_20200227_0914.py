# Generated by Django 3.0.3 on 2020-02-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfirstapp', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='focus_cities',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='user',
            name='focus_constellations',
            field=models.TextField(default='[]'),
        ),
        migrations.AddField(
            model_name='user',
            name='focus_stocks',
            field=models.TextField(default='[]'),
        ),
    ]