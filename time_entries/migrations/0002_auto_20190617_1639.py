# Generated by Django 2.2.1 on 2019-06-17 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_entries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeentry',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
