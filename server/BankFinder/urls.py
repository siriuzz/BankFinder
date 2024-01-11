from django.urls import path, include
from rest_framework import routers
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include("django.contrib.auth.urls")),

        # path('api/', include('router.urls'))
    path('banks/', BankViewSet.as_view({'get': 'getBanks'}), name='bank-list'),
    path('banks/<int:PK>', BankViewSet.as_view({'get': 'getBankById'}), name='bank-detail'),
    path('banks/filter/',BankViewSet.as_view({'get': 'get_banks_filter'})),
    path('banks/create', BankViewSet.as_view({'post': 'createBank'}), name='bank-creation'),
    path('banks/delete/<int:PK>', BankViewSet.as_view({'delete': 'deleteBank'}), name='bank-elimination'),
    path('banks/update/<int:PK>', BankViewSet.as_view({'patch': 'updateBank'}), name='bank-update'),

    path('branches/', BranchViewSet.as_view({'get': 'getBranches'}), name='branch-list'),
    path('branches/<int:PK>', BranchViewSet.as_view({'get': 'getBranchById'}), name='branch-detail'),
    path('branches/create', BranchViewSet.as_view({'post': 'createBranch'}), name='branch-creation'),
    path('branches/delete/<int:PK>', BranchViewSet.as_view({'delete': 'deleteBranch'}), name='branch-elimination'),
    path('branches/update/<int:PK>', BranchViewSet.as_view({'patch': 'updateBranch'}), name='branch-update'),
    
    # path('source_currencies/', SourceCurrencyViewSet.as_view({'get': 'getSourceCurrency'}), name='source_currency-list'),
    # path('source_currencies/<int:PK>', SourceCurrencyViewSet.as_view({'get': 'getSourceCurrencyById'}), name='source_currency-detail'),
    # path('source_currencies/create', SourceCurrencyViewSet.as_view({'post': 'createSourceCurrency'}), name='source_currency-creation'),
    # path('source_currencies/update/<int:PK>', SourceCurrencyViewSet.as_view({'patch': 'updateSourceCurrency'}), name='source_currency-update'),
    # path('source_currencies/delete/<int:PK>', SourceCurrencyViewSet.as_view({'delete': 'deleteSourceCurrency'}), name='source_currency-elimination'),

    # path('target_currencies/', TargetCurrencyViewSet.as_view({'get': 'getTargetCurrency'}), name='target_currency-list'),
    # path('target_currencies/<int:PK>', TargetCurrencyViewSet.as_view({'get': 'getTargetCurrencyById'}), name='target_currency-detail'),
    # path('target_currencies/create', TargetCurrencyViewSet.as_view({'post': 'createTargetCurrency'}), name='target_currency-creation'),
    # path('target_currencies/update/<int:PK>', TargetCurrencyViewSet.as_view({'patch': 'updateTargetCurrency'}), name='target_currency-update'),
    # path('target_currencies/delete/<int:PK>', TargetCurrencyViewSet.as_view({'delete': 'deleteTargetCurrency'}), name='target_currency-elimination'),

    path('currency/', CurrencyViewSet.as_view({'get': 'getCurrency'}), name='currency-list'),
    path('currency/<int:PK>', CurrencyViewSet.as_view({'get': 'getCurrencyById'}), name='currency-detail'),
    path('currency/create', CurrencyViewSet.as_view({'post': 'createCurrency'}), name='currency-creation'),
    path('currency/update/<int:PK>', CurrencyViewSet.as_view({'patch': 'updateCurrency'}), name='currency-update'),
    path('currency/delete/<int:PK>', CurrencyViewSet.as_view({'delete': 'deleteCurrency'}), name='currency-elimination'),

    path('bank_currency_exchange/', BankCurrencyExchangeViewSet.as_view({'get': 'getBankCurrencyExchange'}), name='bank_currency-list'),
    path('bank_currency_exchange/<int:PK>', BankCurrencyExchangeViewSet.as_view({'get': 'getBankCurrencyExchangeById'}), name='bank_currency-detail'),
    path('bank_currency_exchange/create', BankCurrencyExchangeViewSet.as_view({'post': 'createBankCurrencyExchange'}), name='bank_currency-creation'),
    path('bank_currency_exchange/update/<int:PK>', BankCurrencyExchangeViewSet.as_view({'patch': 'updateBankCurrencyExchange'}), name='bank_currency-update'),
    path('bank_currency_exchange/delete/<int:PK>', BankCurrencyExchangeViewSet.as_view({'delete': 'deleteBankCurrencyExchange'}), name='bank_currency-elimination'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('auth/login', UserViewSet.as_view({'post':'login'}), name="Login"),
    path('auth/register', UserViewSet.as_view({'post': 'register'}), name="Register"),
    path('auth/logout/',UserViewSet.as_view({'get':'logout'}),name="Logout"),
    path('is-auth/', UserViewSet.as_view({'get':'check_auth'}), name="check_auth"),
    path('get_csrf_token/', get_csrf_token, name="get_csrf_token"),
    path('user-data/',UserViewSet.as_view({'get':'getUserBySessionId'})),
    path('user/update',UserViewSet.as_view({'patch':'updateUser'}),name="update_user"),
    path('user/change_password',UserViewSet.as_view({'patch':'changePassword'}),name='change_password'),
    path('user/is-username-taken',UserViewSet.as_view({'get':'isUsernameTaken'}),name='isUsernameTaken')
]

urlpatterns += router.urls