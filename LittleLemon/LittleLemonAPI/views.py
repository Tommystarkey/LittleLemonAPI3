# views.py
from .models import *
from .serializers import *
from .permissions import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, action
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination





class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer   
    ordering_fields = ['price', 'category__title']
    search_fields = ['title']
    pagination_class = PageNumberPagination
    page_size = 3
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        # Check if the user is a manager
        if request.user.groups.filter(name='Manager').exists():
            # Only managers can create menu items
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
            return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Check if the user is a manager
        if request.user.groups.filter(name='Manager').exists():
            # Only managers can update menu items
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        # Check if the user is a manager
        if request.user.groups.filter(name='Manager').exists():
            # Only managers can partially update menu items
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        # Check if the user is a manager
        if request.user.groups.filter(name='Manager').exists():
            # Only managers can delete menu items
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsManager])  # returns true or false if manager permission class is satisfied
def managers(request, user_id=None):
    # If a user_id is provided, handle it as a detail view (GET, POST, DELETE for a specific manager)
    if user_id is not None:
        user = get_object_or_404(User, id=user_id)

        if request.method == 'GET':
            # Return details of the specific manager (User) with the provided user_id
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            # Add the user to the 'Manager' group
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message": "User added to managers"}, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            # Remove the user from the 'Manager' group
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({"message": "User removed from managers"}, status=status.HTTP_200_OK)

    # If no user_id is provided, handle it as a list view (GET for all managers, POST to add a new manager)
    elif request.method == 'GET':
        # Return a list of all managers
        managers = Group.objects.get(name="Manager").user_set.all()
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
    # Add a new manager (user) to the 'Manager' group
        username = request.data.get('username')
    
        if username:
            # Try to get an existing user or create a new one
            new_manager, created = User.objects.get_or_create(username=username)

            if created:
                # User was created, add them to the 'Manager' group
                managers = Group.objects.get(name="Manager")
                managers.user_set.add(new_manager)
                return Response({"message": "User added to managers"}, status=status.HTTP_201_CREATED)
            else:
                # User already exists, return an appropriate response
                return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # If none of the conditions are met, return an error response
    return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsManager])
def delivery_crew(request, user_id=None):

    # If a user_id is provided, handle it as a detail view (GET, POST, DELETE for a specific manager)
    if user_id is not None:
        user = get_object_or_404(User,id=user_id)

        #Return details of the specific (User) with the provided user_id
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Add the user to the 'Delivery_Crew' group
        elif request.method == 'POST':
            delivery_crew = Group.objects.get(name="Delivery_Crew")
            delivery_crew.user_set.add(user)
            return Response({"message":"User added to Delivery_Crew"}, status=status.HTTP_201_CREATED)
        
        #remove the user from 'Delivery_Crew' Group
        elif request.method == 'DELETE':
            delivery_crew = Group.objects.get(name="Delivery_Crew")
            delivery_crew.user_set.remove(user)
            return Response({"message": "User removed from Delivery_Crew"}, status=status.HTTP_200_OK)

    # If user_id is not provided, handle it as a list view (GET for all managers, POST to add a new manager)  
    
    # Return a list of all Delivery_Crew
    elif request.method == 'GET':
        delivery_crew = Group.objects.get(name="Delivery_Crew").user_set.all()
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        username = request.data.get('username')
    
        if username:
            # Try to get an existing user or create a new one
            new_delivery_crew, created = User.objects.get_or_create(username=username)

            if created:
                # User was created, add them to the 'Manager' group
                delivery_crew = Group.objects.get(name="Delivery_Crew")
                delivery_crew.user_set.add(new_delivery_crew)
                return Response({"message": "User added to Delivery_Crew"}, status=status.HTTP_201_CREATED)
            else:
                # User already exists, return an appropriate response
                return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # If none of the conditions are met, return an error response
    return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)
  

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #filters the queryset to only include instances of the Cart model where the user field matches the currently authenticated user
        return Cart.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        # Get the current user's cart items
        cart_items = Cart.objects.filter(user=request.user)

        # Create OrderItem instances from cart items
        order_items_data = []
        total_price = 0

        for cart_item in cart_items:
            order_items_data.append({
                'menuitem': cart_item.menuitem.id,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.unit_price,
                'price': cart_item.price
            })

            total_price += cart_item.price

        # Create OrderItem instances
        order_item_serializer = OrderItemSerializer(data=order_items_data, many=True)
        order_item_serializer.is_valid(raise_exception=True)
        order_items = order_item_serializer.save()
        
        # Create Order
        order = Order.objects.create(user=request.user, total=total_price)
        
        # Associate order items with the order
        order.items.set(order_items)
        
        # Delete cart items
        cart_items.delete()
        return Response({"detail": "Order created successfully."}, status=status.HTTP_201_CREATED)
    

    
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['price', 'category__title']
    search_fields = ['title']

    def get_queryset(self):
        # Filter orders based on user role
        if self.request.user.groups.filter(name='Customer').exists():
            return Order.objects.filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='DeliveryCrew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.none()

    def perform_create(self, serializer):
        # Create a new order for the current user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def order_items(self, request, pk=None):
        # Get all items for a specific order
        order = self.get_object()
        if order.user == request.user or request.user.groups.filter(name='Manager').exists():
            order_items = OrderItem.objects.filter(order=order)
            serializer = OrderItemSerializer(order_items, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "You don't have permission to view this order."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['put', 'patch'])
    def update_order(self, request, pk=None):
        # Update the order (status, delivery crew) by a Manager
        order = self.get_object()
        if request.user.groups.filter(name='Manager').exists():
            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"detail": "You don't have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['delete'])
    def delete_order(self, request, pk=None):
        # Delete the order by a Manager
        order = self.get_object()
        if request.user.groups.filter(name='Manager').exists():
            order.delete()
            return Response({"detail": "Order deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You don't have permission to delete this order."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def create_order_item(self, request, pk=None):
        # Get the current user's cart items
        cart_items = Cart.objects.filter(user=request.user)

        # Create OrderItem instances from cart items
        order_items_data = []
        total_price = 0

        for cart_item in cart_items:
            order_items_data.append({
                'order': pk,
                'menuitem': cart_item.menuitem.id,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.unit_price,
                'price': cart_item.price
            })

            total_price += cart_item.price

        # Create OrderItem instances
        order_item_serializer = OrderItemSerializer(data=order_items_data, many=True)
        order_item_serializer.is_valid(raise_exception=True)
        order_items = order_item_serializer.save()

        # Update the total price in the corresponding Order
        order = get_object_or_404(Order, id=pk)
        order.total = total_price
        order.save()

        # Delete cart items
        cart_items.delete()

        return Response({"detail": "Order items created successfully."}, status=status.HTTP_201_CREATED)
