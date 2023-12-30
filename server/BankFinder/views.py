from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from django.middleware.csrf import get_token

from .models import *
from .serializers import *
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm

import logging


def get_csrf_token(request):
    csrf_token=get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

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
        print('hola')
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    
    # @authentication_classes([])
    # @permission_classes([AllowAny])
    def login(self,request):
        user = authenticate(request,username = request.data.get('username'),password= request.data.get('password'))
        print('Result of authenticate:', user)
        if user is not None:
           return JsonResponse({'status': 'success'}, status=200)
        else:
           return JsonResponse({'status': 'failure'}, status=401)

def testHomepage(request):
    return render(request, 'homePage.html', )


def serializerTest(request):
    app = bank.objects.all()
    serializer = BankSerializer(app, many=True)
    return JsonResponse({"banks": serializer.data}, safe=False)


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/register.html', { 'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("loginPage")
        else:

            return render(request, 'registration/register.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect("homePage")