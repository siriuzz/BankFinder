from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly, IsAuthenticated
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from datetime import *

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
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['bank_name']

    def getBanks(self,request):
        banks = bank.objects.all()
        serializer = BankSerializer(banks,many=True)
        return Response(serializer.data)

    def getBankById(self, request, PK=None):
        bank_obj = bank.objects.get(pk=PK)
        serializer = BankSerializer(bank_obj)
        print('hola')
        return Response(serializer.data)
    
    def getBankByName(self,request,bank_name):
        if bank_name:
          filter = bank.objects.filter(bank_name__icontains=bank_name)
        #   filter = bank.objects.filter(bank_name__istartswith=bank_name)
        #   filter = bank.objects.filter(bank_name__iendswith=bank_name)
        #   filter = bank.objects.filter(bank_name__icontains=bank_name)
        #   filter = bank.objects.filter(bank_name__iexact=bank_name)
        
          print(str(filter.query))
          results = filter.values('bank_name')  # Execute the query
          print(results)
          serializer = BankSerializer(filter, many=True)
          return Response({'result':serializer.data})
        else:
          return Response({'error':'No search query provided'})
    
    def createBank(self, request):
        new_Bank = bank(bank_name=request.data.get("bank_name"), website=request.data.get("website"), contact_number=request.data.get("contact_number"))
        try:
            new_Bank.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def updateBank(self, request, PK):
        updated_Bank = bank.objects.get(pk=PK)
        updated_Bank.bank_name = request.data.get("bank_name")
        updated_Bank.website = request.data.get("website")
        updated_Bank.contact_number = request.data.get("contact_number")
        try:
            updated_Bank.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def deleteBank(self, request, PK=None):
        deleted_Bank = bank.objects.get(pk=PK)
        try:
            deleted_Bank.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
        


class BranchViewSet(viewsets.ModelViewSet):
    queryset = branch.objects.all().order_by('-branch_id')
    serializer_class = BranchSerializer
    permission_classes = [permissions.AllowAny]

    def getBranches(self,request):
        branches = branch.objects.all()
        serializer = BranchSerializer(branches, many=True, context={'request': request})
        return Response(serializer.data)

    def getBranchById(self, request, PK=None):
        branches = branch.objects.get(pk=PK)
        serializer = BranchSerializer(branches, context={'request': request})
        return Response(serializer.data)
    
    def createBranch(self, request):
        Bank_id = bank.objects.get(pk=request.data.get("bank_id"))
        new_Branch = branch(
            bank_id=Bank_id,
            branch_name=request.data.get("branch_name"), 
            location=request.data.get("location"), 
            branch_contact_number=request.data.get("branch_contact_number"),
            opening_hour=request.data.get("opening_hour"),
            closing_hour=request.data.get("closing_hour"))
        try:
            new_Branch.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def updateBranch(self, request, PK):
        updated_Branch = branch.objects.get(pk=PK)
        updated_Branch.branch_name = request.data.get('branch_name')
        updated_Branch.location = request.data.get('location')
        updated_Branch.branch_contact_number = request.data.get('branch_contact_number')
        updated_Branch.opening_hour = request.data.get('opening_hour')
        updated_Branch.closing_hour = request.data.get('closing_hour')
        try:
            updated_Branch.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def deleteBranch(self, request, PK=None):
        deleted_Branch = branch.objects.get(pk=PK)
        try:
            deleted_Branch.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
       

class SourceCurrencyViewSet(viewsets.ModelViewSet):
    queryset = source_currency.objects.all()
    serializer_class = SourceCurrencySerializer
    permission_classes = [permissions.AllowAny]

    def getSourceCurrency(self,request):
        source_currencies = source_currency.objects.all()
        serializer = SourceCurrencySerializer(source_currencies, many=True, context={'request': request})
        return Response(serializer.data)

    def getSourceCurrencyById(self, request, PK=None):
        source_currencies = source_currency.objects.get(pk=PK)
        serializer = SourceCurrencySerializer(source_currencies, context={'request': request})
        return Response(serializer.data)
    
    def createSourceCurrency(self, request):
        new_source_currency = source_currency(
            currency_code=request.data.get("currency_code"), 
            currency_name=request.data.get("currency_name"))
        try:
            new_source_currency.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def updateSourceCurrency(self, request, PK):
        updated_source_currency = source_currency.objects.get(pk=PK)
        updated_source_currency.currency_code = request.data.get('currency_code')
        updated_source_currency.currency_name = request.data.get('currency_name')
        try:
            updated_source_currency.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def deleteSourceCurrency(self, request, PK=None):
        deleted_source_currency = source_currency.objects.get(pk=PK)
        try:
            deleted_source_currency.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
        

class TargetCurrencyViewSet(viewsets.ModelViewSet):
    queryset = target_currency.objects.all()
    serializer_class = TargetCurrencySerializer
    permission_classes = [permissions.AllowAny]

    def getTargetCurrency(self,request):
        target_currencies = target_currency.objects.all()
        serializer = TargetCurrencySerializer(target_currencies, many=True, context={'request': request})
        return Response(serializer.data)

    def getTargetCurrencyById(self, request, PK=None):
        target_currencies = target_currency.objects.get(pk=PK)
        serializer = TargetCurrencySerializer(target_currencies, context={'request': request})
        return Response(serializer.data)
    
    def createTargetCurrency(self, request):
        new_target_currency = target_currency(
            currency_code=request.data.get("currency_code"), 
            currency_name=request.data.get("currency_name"))
        try:
            new_target_currency.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def updateTargetCurrency(self, request, PK):
        updated_target_currency = target_currency.objects.get(pk=PK)
        updated_target_currency.currency_code = request.data.get('currency_code')
        updated_target_currency.currency_name = request.data.get('currency_name')
        try:
            updated_target_currency.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def deleteTargetCurrency(self, request, PK=None):
        deleted_target_currency = target_currency.objects.get(pk=PK)
        try:
            deleted_target_currency.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post','get']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'login' or self.action == 'register' or self.action =='check_auth':
           # Solo para esta vista, permitimos el acceso a cualquier usuario
           return [AllowAny()]
        return super().get_permissions()
    
    # @authentication_classes([])
    # @permission_classes([AllowAny])
    def login(self,request):

        user = authenticate(request,username = request.data.get('username'),password= request.data.get('password'))
        print('Result of authenticate:', user)

        if user is not None:
           login(request,user)
           return Response({'status': 'success'} )
        else:
           return Response({'status': 'failure'})

    def register(self, request):
        try:
            user = User.objects.create_user(request.data.get('username'), request.data.get('email'), request.data.get('password'))
            user.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=401)

    def check_auth(self,request):
        try:
            if request.user.is_authenticated:
                return Response({'auth':True},status=200)
            else:
                return Response({'auth':False})
        except Exception as e:
            return Response({'error', str(e)},status=500)

    def logout(self,request):
        try:
            logout(request)
            return Response({'status':'success'})
        except Exception as e:
            return Response({'error', str(e)})





# def testHomepage(request):
#     return render(request, 'homePage.html', )


# def serializerTest(request):
#     app = bank.objects.all()
#     serializer = BankSerializer(app, many=True)
#     return JsonResponse({"banks": serializer.data}, safe=False)