from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('menu',views.menu, name='menu'),
    path('input_form',views.input_form, name='input_form'),
    path('result',views.result, name='result'),
    path('history',views.history, name='history'),
    path('caliculate',views.caliculate, name='caliculate'),
]
