from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('', views.account, name='account'),

]




