from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm


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

