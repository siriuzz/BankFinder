# Generated by Django 5.0 on 2024-01-04 20:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankFinder', '0006_remove_bank_currency_exchange_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_currency_exchange',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 16, 43, 40, 779753), null=True),
        ),
    ]
