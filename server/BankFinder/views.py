from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from django.http import JsonResponse

# Create your views here.
class BankViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = bank.objects.all().order_by('-bank_id')
    serializer_class = BankSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def getBanks(self,request):
        banks = bank.objects.all()
        serializer = BankSerializer(banks,many=True)
        return Response(serializer.data)

    def getBankById(self, request, pk=None):  
        bank_obj = self.get_object()
        serializer = BankSerializer(bank_obj)
        return Response(serializer.data)
