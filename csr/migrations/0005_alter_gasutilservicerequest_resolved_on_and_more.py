# Generated by Django 4.1.7 on 2023-08-13 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csr', '0004_alter_gasutilservicerequest_resolved_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasutilservicerequest',
            name='resolved_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 13, 10, 41, 36, 744586, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='gasutilservicerequest',
            name='service_paid_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 13, 10, 41, 36, 744586, tzinfo=datetime.timezone.utc)),
        ),
    ]
