# Generated by Django 5.0 on 2024-01-04 20:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankFinder', '0005_currency_remove_exchange_rate_source_currency_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank_currency_exchange',
            name='rate',
        ),
        migrations.AddField(
            model_name='bank_currency_exchange',
            name='buying_at',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='bank_currency_exchange',
            name='selling_at',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='bank_currency_exchange',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 16, 34, 17, 640482), null=True),
        ),
    ]
