from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly, IsAuthenticated
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from datetime import *
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
import string
import secrets

from django.db.models import Count, Q
from .models import *
from .serializers import *
from django.http import JsonResponse
import os



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

    def get_banks(self,request):
        banks = bank.objects.prefetch_related('branches').all()
        serializer = BankSerializer(banks,many=True)
        return Response(serializer.data)

    def get_bank_by_id(self, request, PK=None):
        bank_obj = bank.objects.get(pk=PK)
        serializer = BankSerializer(bank_obj)
        # print('hola')
        return Response(serializer.data)
    
    def get_banks_filter(self,request):
        params = request.query_params
        bank_name = params.get('bank_name')
        if bank_name != "" or bank_name is not None:
            filter = bank.objects.filter(bank_name__icontains=bank_name)
            filter = filter.annotate(branches_count=Count('branches'))
        #     filter = bank.objects.filter(bank_name__istartswith=bank_name)
        #     filter = bank.objects.filter(bank_name__iendswith=bank_name)
        #     filter = bank.objects.filter(bank_name__icontains=bank_name)
        #     filter = bank.objects.filter(bank_name__iexact=bank_name)
        #     print(request.query_params.get('city'))
            min_sucursales = params.get('min_sucursales')
            max_sucursales = params.get('max_sucursales')

            if min_sucursales is not None:
                filter = filter.filter(branches_count__gte=min_sucursales)
            if max_sucursales is not None:
                filter = filter.filter(branches_count__lte=max_sucursales)

            page=params.get('page')
            opening_hour=params.get('opening_hour')
            closing_hour=params.get('closing_hour')

            if opening_hour:
                  # Use Q objects to combine conditions with OR logic
                  filter = filter.filter(branches__opening_hour__lte=opening_hour) 
                  
            if closing_hour:
                  # Use Q objects to combine conditions with OR logic
                  filter = filter.filter(branches__closing_hour__gte=closing_hour) 

            currencies = params.get('currencies').split(',')
            # print(currencies)
            if currencies != ['']:
                for i in range(len(currencies)): 
                    filter = filter.filter(bank_currency_exchange__currency_id__currency_code=currencies[i])
                
            items_per_page=params.get('items_per_page')
            paginator = Paginator(filter, items_per_page)
            
            try:
                result_page = paginator.page(page)
            except PageNotAnInteger:
                # print('NAN')
                result_page=paginator.page(1)
            except EmptyPage:
                result_page = paginator.page(paginator.num_pages)
                ##gc211 fd411

            serializer = BankSerializer(result_page, many=True)
            results = filter.values('bank_name', 'branches_count')

              # for banks in serializer:
                  # if branches_count >= min_sucursales and branches_count <= max_sucursales:

        #     print(str(filter.query))
        #     print(results)
            return Response({'result':serializer.data, 'branches_count_result':results, 'total_pages': paginator.num_pages})
        else:
            banks = bank.objects.prefetch_related('branches').all()
            serializer = BankSerializer(banks,many=True)
            return Response(serializer.data)
    
    def create_bank(self, request):
        new_Bank = bank(bank_name=request.data.get("bank_name"), website=request.data.get("website"), contact_number=request.data.get("contact_number"))
        try:
            new_Bank.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def update_bank(self, request, PK):
        try:
            updated_Bank = bank.objects.get(pk=PK)
            updated_Bank.bank_name = request.data.get("bank_name")
            updated_Bank.website = request.data.get("website")
            updated_Bank.contact_number = request.data.get("contact_number")

            updated_Bank.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def delete_bank(self, request, PK=None):
        try:
            deleted_Bank = bank.objects.get(pk=PK)
            deleted_Bank.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
        


class BranchViewSet(viewsets.ModelViewSet):
    queryset = branch.objects.all().order_by('-branch_id')
    serializer_class = BranchSerializer
    permission_classes = [permissions.AllowAny]

    def get_branches(self,request):
        branches = branch.objects.all()
        serializer = BranchSerializer(branches, many=True, context={'request': request})
        return Response(serializer.data)

    def get_branch_by_id(self, request, PK=None):
        branches = branch.objects.get(pk=PK)
        serializer = BranchSerializer(branches, context={'request': request})
        return Response(serializer.data)
    
    def create_branch(self, request):
        try:
            Bank_object = bank.objects.get(pk=request.data.get("bank_id"))

            new_Branch = branch(
                bank_id=Bank_object,
                branch_name=request.data.get("branch_name"), 
                location=request.data.get("location"), 
                branch_contact_number=request.data.get("branch_contact_number"),
                opening_hour=request.data.get("opening_hour"),
                closing_hour=request.data.get("closing_hour"))
            
            new_Branch.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def update_branch(self, request, PK):
        try:
            updated_Branch = branch.objects.get(pk=PK)
            updated_Branch.branch_name = request.data.get('branch_name')
            updated_Branch.location = request.data.get('location')
            updated_Branch.branch_contact_number = request.data.get('branch_contact_number')
            updated_Branch.opening_hour = request.data.get('opening_hour')
            updated_Branch.closing_hour = request.data.get('closing_hour')
            updated_Branch.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def delete_branch(self, request, PK=None):
        try:
            deleted_Branch = branch.objects.get(pk=PK)
            deleted_Branch.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
       

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.AllowAny]

    def get_currency(self,request):
        source_currencies = currency.objects.all()
        serializer = CurrencySerializer(source_currencies, many=True, context={'request': request})
        return Response(serializer.data)

    def get_currency_by_id(self, request, PK=None):
        source_currencies = currency.objects.get(pk=PK)
        serializer = CurrencySerializer(source_currencies, context={'request': request})
        return Response(serializer.data)
    
    def create_currency(self, request):
        try:
            new_currency = currency(
                currency_code=request.data.get("currency_code"), 
                currency_name=request.data.get("currency_name"))
            
            new_currency.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def update_currency(self, request, PK):
        try:
            updated_currency = currency.objects.get(pk=PK)
            updated_currency.currency_code = request.data.get('currency_code')
            updated_currency.currency_name = request.data.get('currency_name')
            updated_currency.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def delete_currency(self, request, PK=None):
        try:
            deleted_currency = currency.objects.get(pk=PK)
            deleted_currency.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
        



class BankCurrencyExchangeViewSet(viewsets.ModelViewSet):
    queryset = bank_currency_exchange.objects.all()
    serializer_class = BankCurrencyExchangeSerializer
    permission_classes = [permissions.AllowAny]

    def get_bank_currency_exchange(self,request):
        bank_currency_exchanges = bank_currency_exchange.objects.all()
        serializer = BankCurrencyExchangeSerializer(bank_currency_exchanges, many=True, context={'request': request})
        return Response(serializer.data)

    def get_bank_currency_exchange_by_id(self, request, PK=None):
        bank_currency_exchanges = bank_currency_exchange.objects.get(pk=PK)
        serializer = BankCurrencyExchangeSerializer(bank_currency_exchanges, context={'request': request})
        return Response(serializer.data)
    
    def create_bank_currency_exchange(self, request):
        try:
            currency_object = currency.objects.get(pk=request.data.get("currency_id"))
            Bank_object = bank.objects.get(pk=request.data.get("bank_id"))

            new_bank_currency_exchange = bank_currency_exchange(
            currency_id=currency_object, 
            bank_id=Bank_object,
            buying_at=request.data.get("buying_at"),
            selling_at=request.data.get("selling_at"),
            last_update=request.data.get("last_update"))
            
            new_bank_currency_exchange.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def update_bank_currency_exchange(self, request, PK):
        try:
            currency_object = currency.objects.get(pk=request.data.get("currency_id"))
            Bank_object = bank.objects.get(pk=request.data.get("bank_id"))

            updated_bank_currency_exchange = bank_currency_exchange.objects.get(pk=PK)
            updated_bank_currency_exchange.currency_id = currency_object
            updated_bank_currency_exchange.bank_id = Bank_object
            updated_bank_currency_exchange.buying_at = request.data.get('buying_at')
            updated_bank_currency_exchange.selling_at = request.data.get('selling_at')
            updated_bank_currency_exchange.last_update = request.data.get('last_update')

            updated_bank_currency_exchange.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
    def delete_bank_currency_exchange(self, request, PK=None):
        try:
            deleted_bank_currency_exchange = bank_currency_exchange.objects.get(pk=PK)
            deleted_bank_currency_exchange.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status':'failed', 'error':str(e)}, status=401)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['post','get','patch']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'login' or self.action == 'register' or self.action =='check_auth' or self.action == 'isUsernameTaken' or self.action=='reset_password':
           # Solo para esta vista, permitimos el acceso a cualquier usuario
           return [AllowAny()]
        return super().get_permissions()
    
    # @authentication_classes([])
    # @permission_classes([AllowAny])
    def login(self,request):

        user = authenticate(request,username = request.data.get('username'),password= request.data.get('password'))

        if user is not None:
           login(request,user)
           return Response({'result': 'success'},status=200 )
        else:
           return Response({'result': 'Usuario o contraseña incorrectos'},status=403)

    def register(self, request):
        try:
            user = User.objects.create_user(username = request.data.get('username'), password = request.data.get('password'), email=request.data.get('email'))
            user.first_name = request.data.get('first_name')
            user.save()
            login(request,user)
            return Response({'status': 'success'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=401)

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
        
    def get_user_by_session_id(self,request):
        session_id = request.COOKIES.get('sessionid')
        if session_id:
            try:
                session = Session.objects.get(session_key=session_id)
                user_id = session.get_decoded().get('_auth_user_id')
                user = User.objects.get(id=user_id)
                
                return Response({
                    "username":user.username,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "last_login":user.last_login
                })
            except Exception as e:
                return Response({"error":e})
        else:
            return Response("Missing session id")
        
    def update_user(self,request):
        session_id = request.COOKIES.get('sessionid')
        if request.user.is_authenticated:
            try:
                session = Session.objects.get(session_key=session_id)
                user_id = session.get_decoded().get('_auth_user_id')
                user = User.objects.get(id=user_id)
                user.username = request.data.get('username',user.username)
                user.email = request.data.get('email',user.email)
                user.first_name = request.data.get('first_name',user.first_name)
                user.last_name = request.data.get('last_name',user.last_name)

                user.save()
                
                return Response({'message':'Usuario actualizado correctamente'})
            except Exception as e:
                return Response({'error':e})
        else:
            return Response({'message':'El usuario no esta autenticado'})
        
    def change_password(self,request):
        # session_id = request.COOKIES.get('sessionid')
        if request.user.is_authenticated:
            try:
                
                user_id = request.user.id
                user = User.objects.get(id=user_id)
                # print(request.data.get('old_password'))
                auth = user.check_password(request.data.get('old_password'))
                authNewPassword = user.check_password(request.data.get('new_password'))
                # print(auth)
                if auth:
                    user.set_password(request.data.get("new_password"))
                    user.save()
                    return Response({'message':'Contraseña actualizada correctamente'})
                elif authNewPassword:
                    return Response({'samePassword':True}, status=401)
                else:
                    return Response({'incorrectPassword':True}, status=401)
            except Exception as e:
                return Response({'error':e})
        else:
            return Response({'message':'El usuario no esta autenticado'})

    def is_username_taken(self,request):
        username = request.GET.get('username')
        # print(request.user.is_authenticated)
        if request.user.is_authenticated:
            currentUser = User.objects.get(username=request.user.username)
            if User.objects.filter(username=username).exclude(username=currentUser).exists():
                    return Response({'taken':True})
        else:
            if User.objects.filter(username=username).exists():
                return Response({'taken':True})
            

        return Response({'taken':False})
    
    def reset_password(self,request):
        recipient_email = request.data.get('email')
        # print(recipient_email)
        
        try:
           user = User.objects.get(email=recipient_email)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'El correo electrónico no está registrado'}, status=400)
        length=10
        characters = string.ascii_letters + string.digits + string.punctuation
        random_string = ''.join(secrets.choice(characters) for _ in range(length))
        try:
            user.set_password(random_string)
            user.save()
        except Exception as e:
            return JsonResponse({'error': 'El correo electrónico no está registrado'}, status=400)
            
        
        subject="Recuperación de contraseña"
        message = (
        f'<h1>Hola, {user.first_name}!</h1>'
        f'<p>Has solicitado restablecer tu contraseña. Utiliza la siguiente contraseña temporal para iniciar sesión:</p>'
        f'<p>Nombre de usuario: {user.username}</p>'
        f'<p>Nueva contraseña: {random_string}</p>'
        )
        from_email=os.getenv('EMAIL_HOST_USER')
        recipient_list = [recipient_email]
        send_mail(subject,message,from_email,recipient_list, html_message=message)
        return Response({'done'})




# def testHomepage(request):
#     return render(request, 'homePage.html', )


# def serializerTest(request):
#     app = bank.objects.all()
#     serializer = BankSerializer(app, many=True)
#     return JsonResponse({"banks": serializer.data}, safe=False)
# class TargetCurrencyViewSet(viewsets.ModelViewSet):
#     queryset = target_currency.objects.all()
#     serializer_class = TargetCurrencySerializer
#     permission_classes = [permissions.AllowAny]

#     def getTargetCurrency(self,request):
#         target_currencies = target_currency.objects.all()
#         serializer = TargetCurrencySerializer(target_currencies, many=True, context={'request': request})
#         return Response(serializer.data)

#     def getTargetCurrencyById(self, request, PK=None):
#         target_currencies = target_currency.objects.get(pk=PK)
#         serializer = TargetCurrencySerializer(target_currencies, context={'request': request})
#         return Response(serializer.data)
    
#     def createTargetCurrency(self, request):
#         try:
#             new_target_currency = target_currency(
#                 currency_code=request.data.get("currency_code"), 
#                 currency_name=request.data.get("currency_name"))
            
#             new_target_currency.save()
#             return JsonResponse({'status': 'success'}, status=200)
#         except Exception as e:
#             return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
#     def updateTargetCurrency(self, request, PK):
#         try:
#             updated_target_currency = target_currency.objects.get(pk=PK)

#             updated_target_currency.currency_code = request.data.get('currency_code')
#             updated_target_currency.currency_name = request.data.get('currency_name')

#             updated_target_currency.save()
#             return JsonResponse({'status': 'success'}, status=200)
#         except Exception as e:
#             return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
#     def deleteTargetCurrency(self, request, PK=None):
#         try:
#             deleted_target_currency = target_currency.objects.get(pk=PK)
#             deleted_target_currency.delete()
#             return JsonResponse({'status': 'success'}, status=200)
#         except Exception as e:
#             return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
        

# class CurrencyExchangeViewSet(viewsets.ModelViewSet):
#     queryset = exchange_rate.objects.all()
#     serializer_class = ExchangeRateSerializer
#     permission_classes = [permissions.AllowAny]

#     def getExchangeRate(self,request):
#         exchange_rates = exchange_rate.objects.all()
#         serializer = ExchangeRateSerializer(exchange_rates, many=True, context={'request': request})
#         return Response(serializer.data)

#     def getExchangeRateById(self, request, PK=None):
#         exchange_rates = exchange_rate.objects.get(pk=PK)
#         serializer = ExchangeRateSerializer(exchange_rates, context={'request': request})
#         return Response(serializer.data)
    
#     def createExchangeRate(self, request):
#         try:
#             Source_currency_object = source_currency.objects.get(pk=request.data.get("source_currency_id"))
#             Target_currency_object = target_currency.objects.get(pk=request.data.get("target_currency_id"))

#             new_exchange_rate = exchange_rate(
#             source_currency_id=Source_currency_object, 
#             target_currency_id=Target_currency_object, 
#             last_update=request.data.get("last_update"))
            
#             new_exchange_rate.save()
#             return JsonResponse({'status': 'success'}, status=200)
#         except Exception as e:
#             return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
#     def updateExchangeRate(self, request, PK):
#         try:
#             Source_currency_object = source_currency.objects.get(pk=request.data.get("source_currency_id"))
#             Target_currency_object = target_currency.objects.get(pk=request.data.get("target_currency_id"))

#             updated_exchange_rate = exchange_rate.objects.get(pk=PK)
#             updated_exchange_rate.source_currency_id = Source_currency_object
#             updated_exchange_rate.target_currency_id = Target_currency_object
#             updated_exchange_rate.last_update = request.data.get('last_update')

#             updated_exchange_rate.save()
#             return JsonResponse({'status': 'success'}, status=200)
#         except Exception as e:
#             return JsonResponse({'status':'failed', 'error':str(e)}, status=401)
    
#     def deleteExchangeRate(self, request, PK=None):
#         try:
#             deleted_exchange_rate = exchange_rate.objects.get(pk=PK)
#             deleted_exchange_rate.delete()
#             return JsonResponse({'status': 'success'}, status=200)
#         except Exception as e:
#             return JsonResponse({'status':'failed', 'error':str(e)}, status=401)