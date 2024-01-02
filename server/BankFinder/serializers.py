from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class BankSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=bank
        fields=['bank_id','bank_name','website','contact_number']
        
class BranchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=branch
        fields=['bank_id','branch_id','branch_name','location','branch_contact_number','opening_hour','closing_hour']
        
class SourceCurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=source_currency
        fields=['currency_code','currency_name']
        
class TargetCurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=target_currency
        fields=['currency_code','currency_name']

class ExchangeRateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=exchange_rate
        fields=['exchange_rate_id','source_currency_id','target_currency_id','last_update']

class BankExchangeRate(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=exchange_rate
        fields=['bank_id', 'exchange_rate_id', 'rate', 'last_update']
        