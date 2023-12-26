from django.urls import path
from . import views
from .views import *

from rest_framework.authtoken.views import obtain_auth_token

#/////////////////////////////////////////////#
#//include trailing slash to avoid headaches//#
#/////////////////////////////////////////////#


urlpatterns = [

    path('menu-items/', MenuItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='menu-item-list'),
    path('menu-items/<int:pk>/', MenuItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='menu-item-detail'),
    # path('groups/manager/users/', managers, name='manage_managers'),

    path('groups/managers/users/', views.managers),
    path('groups/managers/users/<int:user_id>', views.managers),
    path('groups/delivery_crew/users/', views.delivery_crew),
    path('groups/delivery_crew/users/<int:user_id>', views.delivery_crew),

    path('cart/', CartViewSet.as_view({'get': 'list', 'post': 'create'}), name='cart-list'),
    path('cart/<int:pk>/', CartViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='cart-detail'),
    path('cart/create_order/', CartViewSet.as_view({'post': 'create_order'}), name='cart-create-order'),
    

    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('orders/<int:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='order-detail'),

    path('api-token-auth/', obtain_auth_token),
    #this automatically generated end point from rest_framework only accepts POST calls
]
