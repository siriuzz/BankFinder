from rest_framework import serializers
from .models import *

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model=bank
        fields=('bank_name','website','contact_number')