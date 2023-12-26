"""
URL configuration for LittleLemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from djoser.views import UserViewSet

urlpatterns = [
    #default patterns
    path('admin/', admin.site.urls),    #spuperuser: admin - admin@littlelemon.co.uk, password: coursera123,
    path('api/', include('LittleLemonAPI.urls')),

    #authorizations patterns
    path('api/users/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('api/users/me/', UserViewSet.as_view({'get': 'retrieve'}), name='user-profile'),

    #djoser patterns
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
