# Generated by Django 3.2.3 on 2021-05-31 06:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('slot', '0005_auto_20210531_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='time',
            field=models.DateField(default=datetime.date(2021, 5, 31)),
        ),
        migrations.AlterField(
            model_name='user',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 0, 59, 36, 677610, tzinfo=utc)),
        ),
    ]
