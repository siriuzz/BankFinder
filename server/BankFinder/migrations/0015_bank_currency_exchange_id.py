# Generated by Django 5.0 on 2024-01-11 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankFinder', '0014_auto_20240111_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank_currency_exchange',
            name='id',
            field=models.BigAutoField( primary_key=True, serialize=False, unique=True),
        ),
    ]