from django.contrib.auth.views import LogoutView
from django.urls import path

from api.views import Convert, Currency

app_name = 'api'

urlpatterns = [
    path('currency/', Currency.as_view(), name='currency'),
    path('convert/', Convert.as_view(), name='convert'),
]
