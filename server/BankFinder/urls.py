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