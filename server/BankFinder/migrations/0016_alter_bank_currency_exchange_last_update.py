# Generated by Django 5.0 on 2024-01-11 16:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankFinder', '0015_bank_currency_exchange_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_currency_exchange',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 11, 12, 54, 1, 469629), null=True),
        ),
    ]
