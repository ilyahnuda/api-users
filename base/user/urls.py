from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    path('transactions/', ListCreateTransaction.as_view(), name='transactions'),
    path('transactions/<int:id>', DetailTransaction.as_view(), name='transaction'),
    path('categories/', ListCreateCategory.as_view(), name='categories'),
    path('categories/<int:id>', DetailCategory.as_view(), name='category'),
    path('users/<int:id>', DetailUser.as_view(), name='user'),
    path('users/', ListCustomUser.as_view(), name='users'),
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
