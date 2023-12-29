from django.urls import path, include
from rest_framework import routers
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()

urlpatterns = [
    path('register', sign_up, name="registerPage"),
    path('', include("django.contrib.auth.urls")),

        # path('api/', include('router.urls'))
    path('banks/', BankViewSet.as_view({'get': 'getBanks'}), name='bank-list'),
    path('banks/<int:pk>', BankViewSet.as_view({'get': 'getBankById'}), name='bank-detail'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

urlpatterns += router.urls