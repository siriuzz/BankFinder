# Generated by Django 5.0 on 2024-01-10 18:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankFinder', '0011_alter_bank_currency_exchange_last_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_currency_exchange',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 10, 14, 29, 54, 166230), null=True),
        ),
    ]
