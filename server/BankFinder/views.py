from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializer import BankSerializer

# Create your views here.
@api_view(['GET'])
def getData(request):
    app = bank.objects.all()
    serializer = BankSerializer
