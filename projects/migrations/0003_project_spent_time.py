# Generated by Django 2.2.1 on 2019-06-17 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20190603_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='spent_time',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
