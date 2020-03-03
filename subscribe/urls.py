from django.urls import path

from subscribe import views
from subscribe import forms
from subscribe.views import *

urlpatterns = [
    path('', views.subscribe, name = 'subscribe'),
]