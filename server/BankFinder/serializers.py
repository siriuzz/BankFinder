from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

        
class BranchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=branch
        fields=['bank_id','branch_id','branch_name','location','branch_contact_number','opening_hour','closing_hour']
        
class BankSerializer(serializers.HyperlinkedModelSerializer):    
    branches = serializers.SerializerMethodField()
    currency_exchanges = serializers.SerializerMethodField()

    class Meta:
        model=bank
        fields=['bank_id','bank_name','website','contact_number','logo','branches','currency_exchanges']
        
    def get_branches(self, obj):
        branches = branch.objects.filter(bank_id=obj)
        branch_serializer = BranchSerializer(branches, many=True, context={'request': self.context.get('request')})
        return branch_serializer.data
    
    def get_currency_exchanges(self,obj):
        currency_exchanges = bank_currency_exchange.objects.filter(bank_id=obj)
        currency_exchanges_serializer = BankCurrencyExchangeSerializer(currency_exchanges, many=True, context={'request': self.context.get('request')})
        return currency_exchanges_serializer.data
        
class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=currency
        fields=['currency_id','currency_code','currency_name']
        
# class TargetCurrencySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=target_currency
#         fields=['target_currency_id','currency_code','currency_name']

# class ExchangeRateSerializer(serializers.HyperlinkedModelSerializer):
#     source_currency_id = serializers.HyperlinkedRelatedField(view_name='source_currency-detail', lookup_url_kwarg='PK', lookup_field='source_currency_id', read_only=True)
#     target_currency_id = serializers.HyperlinkedRelatedField(view_name='target_currency-detail', lookup_url_kwarg='PK', lookup_field='target_currency_id', read_only=True) 
    
#     class Meta:
#         model=exchange_rate
#         fields=['exchange_rate_id','source_currency_id','target_currency_id','last_update']

class BankCurrencyExchangeSerializer(serializers.HyperlinkedModelSerializer):
    bank_id = serializers.HyperlinkedRelatedField(view_name='bank-detail', lookup_url_kwarg='PK', lookup_field='bank_id', read_only=True)
    currency_id = serializers.HyperlinkedRelatedField(view_name='currency-detail', lookup_url_kwarg='PK', lookup_field='currency_id', read_only=True) 
    buying_at = serializers.CharField(read_only=False)
    selling_at = serializers.CharField(read_only=False)
    class Meta:
        model=bank_currency_exchange
        fields=['bank_id', 'currency_id', 'buying_at', 'selling_at', 'last_update']
        
        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields=['username','password','email','first_name','last_name']
        