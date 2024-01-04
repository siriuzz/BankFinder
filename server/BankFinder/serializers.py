from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

        
class BranchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=branch
        fields=['bank_id','branch_id','branch_name','location','branch_contact_number','opening_hour','closing_hour']
        
class BankSerializer(serializers.HyperlinkedModelSerializer):    
    branches = serializers.SerializerMethodField()
    class Meta:
        model=bank
        fields=['bank_id','bank_name','website','contact_number','logo','branches']
        
    def get_branches(self, obj):
        branches = branch.objects.filter(bank_id=obj)
        branch_serializer = BranchSerializer(branches, many=True, context={'request': self.context.get('request')})
        return branch_serializer.data
        
class SourceCurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=source_currency
        fields=['source_currency_id','currency_code','currency_name']
        
class TargetCurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=target_currency
        fields=['target_currency_id','currency_code','currency_name']

class ExchangeRateSerializer(serializers.HyperlinkedModelSerializer):
    source_currency_id = serializers.HyperlinkedRelatedField(view_name='source_currency-detail', lookup_url_kwarg='PK', lookup_field='source_currency_id', read_only=True)
    target_currency_id = serializers.HyperlinkedRelatedField(view_name='target_currency-detail', lookup_url_kwarg='PK', lookup_field='target_currency_id', read_only=True) 
    
    class Meta:
        model=exchange_rate
        fields=['exchange_rate_id','source_currency_id','target_currency_id','last_update']

class BankExchangeRateSerializer(serializers.HyperlinkedModelSerializer):
    bank_id = serializers.HyperlinkedRelatedField(view_name='bank-detail', lookup_url_kwarg='PK', lookup_field='bank_id', read_only=True)
    exchange_rate_id = serializers.HyperlinkedRelatedField(view_name='exchange_rate-detail', lookup_url_kwarg='PK', lookup_field='exchange_rate_id', read_only=True) 
    rate = serializers.CharField(read_only=False)
    
    class Meta:
        model=exchange_rate
        fields=['bank_id', 'exchange_rate_id', 'rate', 'last_update']
        