from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect

# Custom logout to redirect to login page

def custom_logout_view(request):
    logout(request)
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom logout route
    path('accounts/logout/', custom_logout_view, name='logout'),

    # Django auth routes: login, password change, etc.
    path('accounts/', include('django.contrib.auth.urls')),

    # Application routes: home, signup, rewards, balance
    path('', include('base.urls')),
]
