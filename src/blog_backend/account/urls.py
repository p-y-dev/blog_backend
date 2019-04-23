from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account, name='account'),
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
    path('reset_password', views.reset_password, name='reset_password'),
]
