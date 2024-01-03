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
    path('banks/<bank_name>',BankViewSet.as_view({'get': 'getBankByName'})),
    path('banks/create', BankViewSet.as_view({'post': 'createBank'}), name='bank-creation'),
    path('banks/delete/<int:PK>', BankViewSet.as_view({'delete': 'deleteBank'}), name='bank-elimination'),
    path('banks/update/<int:PK>', BankViewSet.as_view({'patch': 'updateBank'}), name='bank-update'),

    path('branches/', BranchViewSet.as_view({'get': 'getBranches'}), name='branch-list'),
    path('branches/<int:PK>', BranchViewSet.as_view({'get': 'getBranchById'}), name='branch-detail'),
    path('branches/create', BranchViewSet.as_view({'post': 'createBranch'}), name='branch-creation'),
    path('branches/delete/<int:PK>', BranchViewSet.as_view({'delete': 'deleteBranch'}), name='branch-elimination'),
    path('branches/update/<int:PK>', BranchViewSet.as_view({'patch': 'updateBranch'}), name='branch-update'),

    path('source_currencies/', SourceCurrencyViewSet.as_view({'get': 'getSourceCurrency'}), name='source_currency-list'),
    path('source_currencies/<int:PK>', SourceCurrencyViewSet.as_view({'get': 'getSourceCurrencyById'}), name='source_currency-detail'),
    path('source_currencies/create', SourceCurrencyViewSet.as_view({'post': 'createSourceCurrency'}), name='source_currency-creation'),
    path('source_currencies/update/<int:PK>', SourceCurrencyViewSet.as_view({'patch': 'updateSourceCurrency'}), name='source_currency-update'),
    path('source_currencies/delete/<int:PK>', SourceCurrencyViewSet.as_view({'delete': 'deleteSourceCurrency'}), name='source_currency-elimination'),

    path('target_currencies/', TargetCurrencyViewSet.as_view({'get': 'getTargetCurrency'}), name='target_currency-list'),
    path('target_currencies/<int:PK>', TargetCurrencyViewSet.as_view({'get': 'getTargetCurrencyById'}), name='target_currency-detail'),
    path('target_currencies/create', TargetCurrencyViewSet.as_view({'post': 'createTargetCurrency'}), name='target_currency-creation'),
    path('target_currencies/update/<int:PK>', TargetCurrencyViewSet.as_view({'patch': 'updateTargetCurrency'}), name='target_currency-update'),
    path('target_currencies/delete/<int:PK>', TargetCurrencyViewSet.as_view({'delete': 'deleteTargetCurrency'}), name='target_currency-elimination'),

    path('exchange_rates/', ExchangeRateViewSet.as_view({'get': 'getExchangeRate'}), name='exchange_rate-list'),
    path('exchange_rates/<int:PK>', ExchangeRateViewSet.as_view({'get': 'getExchangeRateById'}), name='exchange_rate-detail'),
    path('exchange_rates/create', ExchangeRateViewSet.as_view({'post': 'createExchangeRate'}), name='exchange_rate-creation'),
    path('exchange_rates/update/<int:PK>', ExchangeRateViewSet.as_view({'patch': 'updateExchangeRate'}), name='exchange_rate-update'),
    path('exchange_rates/delete/<int:PK>', ExchangeRateViewSet.as_view({'delete': 'deleteExchangeRate'}), name='exchange_rate-elimination'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('auth/login', UserViewSet.as_view({'post':'login'}), name="Login"),
    path('auth/register', UserViewSet.as_view({'post': 'register'}), name="Register"),
    path('auth/logout/',UserViewSet.as_view({'get':'logout'}),name="Logout"),
    path('is-auth/', UserViewSet.as_view({'get':'check_auth'}), name="check_auth"),
    path('get_csrf_token/', get_csrf_token, name="get_csrf_token")
    
]

urlpatterns += router.urls