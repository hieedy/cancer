# Generated by Django 3.2 on 2021-05-25 05:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_auto_20210525_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='myappointment',
            name='app_date',
            field=models.DateField(default=datetime.date(2021, 5, 25)),
            preserve_default=False,
        ),
    ]
