# urls.py example
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.authView, name='signup'),
    path('get_login_reward/', views.get_login_reward, name='get_login_reward'),
    path('check_balance/', views.check_balance, name='check_balance'),
]
