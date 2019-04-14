from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('send_confirm_email', views.send_confirm_email, name='send_confirm_email'),
    path('confirm_email', views.confirm_email, name='confirm_email'),
]
