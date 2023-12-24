from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from .models import *
from .serializers import BankSerializer

# Create your views here.
class BankViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = bank.objects.all().order_by('-bank_id')
    serializer_class = BankSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def getData(request):
    app = bank.objects.all()
    serializer = BankSerializer
