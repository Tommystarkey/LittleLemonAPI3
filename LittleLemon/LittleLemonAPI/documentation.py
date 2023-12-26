#this code doesn't do anything#
##it helps me understand how the code works##
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


"""
    ideas to make project more presentable.

    strip back all permissions.

    customers can log in. --end point
        browse the menu.
        add items to the cart. --end point
        place orders

    staff can log in --end point
        update menu --end point
        view orders
        select order as complete:
            -deletes order
            -sends message to customer saying order was completed
    
    work on front end styling

"""


class MenuItemViewSet(viewsets.ModelViewSet):
#defines Class that inherits from ModelViewSet
    queryset = MenuItem.objects.all()
    #This line specifies the default queryset for the view. In this case, it fetches all instances of the MenuItem
    serializer_class = MenuItemSerializer
    #This line specifies the serializer class that should be used to serialize and deserialize instances of the MenuItem model.
    permission_classes = [IsAuthenticated]
    #This line specifies the permission classes that will be used to determine whether a user has permission to perform certain actions
    ordering_fields = ['price', 'category__title']
    #This line defines the fields by which the queryset can be ordered.
    search_fields = ['title']
    #This line defines the fields on which the view should support search functionality.

    def list(self, request, *args, **kwargs):
    # defines method named list that take as parameters
    # an instance of itself, the request object, (args-used to collect any additional positional arguments passed to the method. In the case of the list method,)
    #**kwargs: This is used to collect any additional keyword arguments passed to the method
        return super().list(request, *args, **kwargs)
    #Returns a temporary object of the superclass, allowing you to call its methods. (.list(request, *args, **kwargs))
    #In the case of a Django REST Framework viewset, this is likely calling the list method provided by the ListModelMixin

    def create(self, request, *args, **kwargs):
    #defiens create function that takes as arguments (an instance of itself,
    #the request, *args: Additional positional arguments (not explicitly named),
    #**kwargs: Additional keyword arguments (not explicitly named) )
        if request.user.groups.filter(name='Manager').exists():
            """
                request.user: This retrieves the user object associated with the current request,
                .groups: This is an attribute of the user model in Django that represents the groups to which the user belongs,
                .filter(name='Manager'): This filters the groups to only include those with the name 'Manager,
                .exists(): This method returns True if there is at least one group that matches the specified filter criteria ('Manager' in this case) and False otherwise
            """
            return super().create(request, *args, **kwargs)
            #calls the create method of the superclass.
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            #returns HTTP response object with 403 status code

    def retrieve(self, request, *args, **kwargs):
    #defines method that takes as arguments( an instance of itself, extra positional arguments, and any keywords )
            return super().retrieve(request, *args, **kwargs)
            #returns the retrieve method of the super class


    def update(self, request, *args, **kwargs):
        # Check if the user is a manager
        if request.user.groups.filter(name='Manager').exists():
            # Only managers can update menu items
            return super().update(request, *args, **kwargs)
            # If the user is a manager, this line calls the update method of the superclass (ModelViewSet).
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            #f the user is not a manager, this line returns a Forbidden HTTP response (HTTP 403 status code)

    def partial_update(self, request, *args, **kwargs):
        # Check if the user is a manager
        if request.user.groups.filter(name='Manager').exists():
            # Only managers can partially update menu items
            return super().partial_update(request, *args, **kwargs)
            #returns a call to the partial update method of the superclass
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            #if the user is not a manager, this line returns a Forbidden HTTP response (HTTP 403 status code)

    def destroy(self, request, *args, **kwargs):
        # Check if the user is a manager
        if request.user.groups.filter(name='Manager').exists():
            # Only managers can delete menu items
            return super().destroy(request, *args, **kwargs)
            #returns a call to the partial update method of the superclass
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            #if the user is not a manager, this line returns a Forbidden HTTP response (HTTP 403 status code)



"""
how the @api_view decorator works:

    A decorator is essentially a function that takes another function as its argument

    The decorator takes a list of HTTP methods as an argument,
    It ensures that the decorated view function can only be accessed using the specified HTTP methods,

    The decorated function receives a request object as its first parameter,
    This request object provides information about the incoming HTTP request,

    The decorated function is expected to return a DRF Response object,
    This Response object represents the HTTP response that will be sent back to the client,
"""
@api_view(['GET', 'POST', 'DELETE'])
#specifies that the decorated function (in this case, the managers function) can only be accessed through HTTP methods such as GET, POST, and DELETE
#A decorator is essentially a function that takes another function as its argument
@permission_classes([IsManager])
#only users who satisfy the conditions specified in the IsManager permission class will be granted access to this view
#if denied  Django REST Framework will return a response with a 403 Forbidden status code
def managers(request, user_id=None):
# If a user_id is provided, handle it as a detail view (GET, POST, DELETE for a specific manager)
    """
        defines a function named managers,
        recieves a request object as a parameter,
        does not take optional user_ID parameter,
    """
    if user_id is not None:
    #checks whether the variable user_id is not equal to None
    # ie if a user_id is included in the request object run through this nested conditional loop
        user = get_object_or_404(User, id=user_id)
        """
       (user, id=user_id) is a Django shortcut that attempts to retrieve a single object from the database based on certain criteria,
       the user_id comes from the URL parameters of the request object
       if the object is not found, it raises a 404 HTTP response,

        """

        if request.method == 'GET':
            #checks whether the HTTP method used for the current request is a GET method
            serializer = UserSerializer(user)
            """
            user is a Django model instance representing a user.
            "UserSerializer(user)" creates an instance of the UserSerializer class and passes the user object to its constructor.
            This instance of the serializer is used to convert the user object into a serialized format,
            the serialized data is stored as a variable named serializer.
            """
            return Response(serializer.data, status=status.HTTP_200_OK)
            #Returns a JSON response containing the serialized data from the serializer instance along with a 200 status code (OK)
        
        elif request.method == 'POST':
        #checks whether the HTTP method used for the current request is a GET method
            managers = Group.objects.get(name="Manager")
            #This line retrieves the group with the name "Manager" from the database
            #objects is a manager that provides a set of database query methods
            #group is a django model representing the user group
            managers.user_set.add(user)
            #user_set manager provided by Django for the Group model. It allows you to manage the users associated with a particular group
            #.add(user): This method is used to add a user
            return Response({"message": "User added to managers"}, status.HTTP_201_CREATED)
            #retruns JSON string response with a 201 status code

        elif request.method == 'DELETE':
            #checks whether the HTTP method used for the current request is a DELETE method
            managers = Group.objects.get(name="Manager")
            #This line retrieves the group with the name "Manager" from the database
            managers.user_set.remove(user)
            #this lines uses user_set method to remove specified user from the database
            return Response({"message": "User removed from managers"}, status.HTTP_200_OK)
            #retruns JSON string response with a 200 status code

    #If no user_id is provided,
    #continue out of nested conditional statment and run through the outer conditional methods.

    elif request.method == 'GET':
    #checks whether the HTTP method used for the current request is a GET method
        managers = Group.objects.get(name="Manager").user_set.all()
        #This line retrieves the group with the name "Manager" from the database
        serializer = UserSerializer(managers, many=True)
        #serializes the instance of the managers model
        #many=True indicates the instance is handelling a collection not a single instance
        return Response(serializer.data, status.HTTP_200_OK)
        #returns the serialized data as part of the request object with a 200 status code

    elif request.method == 'POST':
    # This block of code is checking if the HTTP request method is a POST request
        username = request.data.get('username')
        if username:
        #Here, it checks if a username was provided in the POST request. If a username is present
            # Try to get an existing user or create a new one
            new_manager, created = User.objects.get_or_create(username=username)
            #The get_or_create method is a Django ORM (Object-Relational Mapping) function that tries to fetch a record,
            #from the database based on specified parameters (in this case, the username). 

            if created:
            #If a new user was created (created=True)
                managers = Group.objects.get(name="Manager")
                #The code then fetches the "Manager" group
                managers.user_set.add(new_manager)
                #and adds the newly created usee
                return Response({"message": "User added to managers"}, status=status.HTTP_201_CREATED)
            #Finally, it returns a JSON response indicating success and a status code of 201 (HTTP_CREATED).
            else:
                return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
                # else it returns a JSON response indicating that the user already exists and returns a status code of 400

    # If none of the conditions are met, return an error response
    return Response({"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)



class IsManager(BasePermission):
#IsManager is a custom permission class that inherits from BasePermission, which is provided by DRF
    def has_permission(self, request, view):
        #the has_permission method checks if the user making the request belongs to the "Manager" group
        return request.user.groups.filter(name='Manager').exists()
        #If the user is in the "Manager" group, the method returns True, indicating that the user has permission
    


@api_view(['GET', 'POST', 'DELETE'])
#specifies that the decorated function (in this case, the managers function) can only be accessed through HTTP methods such as GET, POST, and DELETE
#A decorator is essentially a function that takes another function as its argument
class CartViewSet(viewsets.ModelViewSet):
#defines class that inherits from ModelViewSet Class
    queryset = Cart.objects.all()
    #This line specifies the default queryset for the view. In this case, it fetches all instances of the Cart Model
    serializer_class = CartSerializer
    #specifies the serializer for the view
    permission_classes = [IsAuthenticated]
    #checks if the user is authenticated
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
        #This method overrides the default get_queryset method provided by the ModelViewSet class
        #class. It filters the queryset to only include instances of the Cart model where the user field matches the currently authenticated user
        """
            self: Refers to the instance of the CartViewSet class.
            self.request: Represents the current HTTP request.
            self.request.user: Represents the user associated with the current request (assuming authentication is enabled).
        """

    @action(detail=False, methods=['post'])
    #The @action decorator in Django REST framework is used to define custom actions within a ViewSet
    #detail=False: This indicates that the action is not associated with a specific instance of the resource
    #methods=['post']: This specifies the HTTP methods allowed for this action
    def create_order(self, request):
        # defines function definition thats takes an instance of itself and the request object as parameters
        cart_items = Cart.objects.filter(user=request.user)
        #This line retrieves all the Cart objects associated with the current user (request.user), and asigns it to the variable cart_items
        order_items_data = []
        #This is a list that will store dictionaries, each representing an OrderItem
        total_price = 0

        for cart_item in cart_items:
        #The for loop iterates through each cart_item in cart_items
        #and creates a dictionary with the necessary information to create an OrderItem
            order_items_data.append({
                'menuitem': cart_item.menuitem.id,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.unit_price,
                'price': cart_item.price
            })

            total_price += cart_item.price
            """
                total_price: This variable is used to calculate the total price of the order,
                t's incremented in each iteration of the loop by adding the price of the current cart_item
            """

        # Create OrderItem instances
        order_item_serializer = OrderItemSerializer(data=order_items_data, many=True)
        #This line initializes an instance of the OrderItemSerializer class.
        #it takes the list of dictionaries (order_items_data) as data and specifies many=True because we are dealing with multiple items
        order_item_serializer.is_valid(raise_exception=True)
        #This line checks if the data provided to the serializer is valid
        #It invokes the is_valid method of the serializer. If the data is not valid, it would raise a validation error, and raise_exception=True ensures that the error is raised immediately
        order_items = order_item_serializer.save()
        """
        If the data is valid, this line saves the data and creates OrderItem instances.
        The save method of the serializer is responsible for creating the objects in the database.
        The instances are then stored in the order_items variable.  
        """

        order = Order.objects.create(user=request.user, total=total_price)
        #This line creates a new Order instance in the database
        #It associates the order with the current user (request.user)
        #and sets the total price of the order (total_price)
        order.items.set(order_items)
        #This line associates the OrderItem instances (order_items) with the created Order
        cart_items.delete()
        #deletes the cart items
        return Response({"detail": "Order created successfully."}, status=status.HTTP_201_CREATED)
        # returns JSON response with 201 status code



class OrderViewSet(ModelViewSet):
#defines class that inherits from ModelViewSet
    queryset = Order.objects.all()
    #defines queryset
    serializer_class = OrderSerializer
    #specifies serializer
    permission_classes = [IsAuthenticated]
    #check for authentication
    ordering_fields = ['price', 'category__title']
    #specifies ordering fields
    search_fields = ['title']
    #specifies search fields

    def get_queryset(self):
        # Filter orders based on user role
        if self.request.user.groups.filter(name='Customer').exists():
            return Order.objects.filter(user=self.request.user)
            #If the user belongs to the 'Customer' group, it returns a queryset of orders where the user field matches the current user
        elif self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
            #If the user belongs to the 'Manager' group, it returns all orders
        elif self.request.user.groups.filter(name='DeliveryCrew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
            #If the user belongs to the 'DeliveryCrew' group, it returns a queryset of orders where the delivery_crew field matches the current user
        else:
            return Order.objects.none()
            #If the user doesn't belong to any of the specified groups or is not authenticated, it returns an empty queryset

    def perform_create(self, serializer):
        ## Create a new order for the current user
        serializer.save(user=self.request.user)
        #It overrides the default behavior to set the user of the order to the current authenticated user (self.request.user).


    @action(detail=True, methods=['get'])
    #This action is an endpoint that retrieves all items for a specific order.
    #detail=True argument indicates that this action is associated with a single instance of the resource 
    def order_items(self, request, pk=None):
    #pk being None would mean that the action is not targeting a specific order (it's a more general operation)
        order = self.get_object()
        if order.user == request.user or request.user.groups.filter(name='Manager').exists():
        #The action checks if the requesting user is the owner of the order or belongs to the 'Manager' group.
            order_items = OrderItem.objects.filter(order=order)
            #retrieves data
            serializer = OrderItemSerializer(order_items, many=True)
            #serializes data
            return Response(serializer.data)
            #returns serialized data
            #If either condition is true, the user has permission to view the order items
        else:
            return Response({"detail": "You don't have permission to view this order."}, status=status.HTTP_403_FORBIDDEN)
            #If the user does not have permission, a response is returned with a 403 Forbidden status

    @action(detail=True, methods=['put', 'patch'])
    #This decorator indicates that this action is intended to update a specific instance (detail=True) 
    #and supports HTTP PUT and PATCH methods.
    def update_order(self, request, pk=None):
    #This is the method for the update_order action within the OrderViewSet
    #It takes the standard parameters for a method in a Django class-based view or viewset (self, request, and pk) 
    #pk=None: This specifies that the pk parameter is optional, and if not provided, it defaults to None
        order = self.get_object()
        #This retrieves the specific order instance based on the provided primary key (pk)
        if request.user.groups.filter(name='Manager').exists():
        #Checks if the user making the request belongs to the 'Manager' group
            serializer = self.get_serializer(order, data=request.data, partial=True)
            #Creates a serializer instance for the order, using the data from the request. The partial=True parameter allows for partial updates (PATCH
            serializer.is_valid(raise_exception=True)
            #Checks if the serializer is valid. If not, it raises a validation exception, which will return a 400 Bad Request response
            serializer.save()
            #Saves the updated data
            return Response(serializer.data)
            #f the update is successful, it returns a response with the serialized data of the updated order.
        else:
            return Response({"detail": "You don't have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)
            #If the user making the request is not a manager, it returns a 403 Forbidden response.



    @action(detail=True, methods=['delete'])
    #This decorator indicates that this action is intended to update a specific instance (detail=True) 
    #and supports the DELETE method.
    def delete_order(self, request, pk=None):
    #This is the method for the update_order action within the OrderViewSet
    #It takes the standard parameters for a method in a Django class-based view or viewset (self, request, and pk) 
    #pk=None: This specifies that the pk parameter is optional, and if not provided, it defaults to None
        order = self.get_object()
        #This retrieves the specific order instance based on the provided primary key (pk)
        if request.user.groups.filter(name='Manager').exists():
        #Checks if the user making the request belongs to the 'Manager' group
            order.delete()
            #the order is deleted
            return Response({"detail": "Order deleted successfully."}, status=status.HTTP_200_OK)
            #returns JSON string with 200 status code
        else:
            return Response({"detail": "You don't have permission to delete this order."}, status=status.HTTP_403_FORBIDDEN)
            #if user is not manager return 403 forbidden code

    @action(detail=True, methods=['post'])
    ##The @action decorator in Django REST framework is used to define custom actions within a ViewSet
    #detail=False: This indicates that the action is not associated with a specific instance of the resource
    #methods=['post']: This specifies the HTTP methods allowed for this action
    def create_order_item(self, request, pk=None):
        # defines function definition thats takes an instance of itself and the request object as parameters
        #pk=None: This specifies that the pk parameter is optional, and if not provided, it defaults to None
        cart_items = Cart.objects.filter(user=request.user)
        #This line retrieves all the Cart objects associated with the current user (request.user), and asigns it to the variable cart_items
        order_items_data = []
         #This is a list that will store dictionaries, each representing an OrderItem
        total_price = 0

        for cart_item in cart_items:
        #The for loop iterates through each cart_item in cart_items
        #and creates a dictionary with the necessary information to create an OrderItem
            order_items_data.append({
                'order': pk,
                'menuitem': cart_item.menuitem.id,
                'quantity': cart_item.quantity,
                'unit_price': cart_item.unit_price,
                'price': cart_item.price
            })

            total_price += cart_item.price
            """
                total_price: This variable is used to calculate the total price of the order,
                t's incremented in each iteration of the loop by adding the price of the current cart_item
            """

        # Create OrderItem instances
        order_item_serializer = OrderItemSerializer(data=order_items_data, many=True)
         #This line initializes an instance of the OrderItemSerializer class.
        #it takes the list of dictionaries (order_items_data) as data and specifies many=True because we are dealing with multiple items
        order_item_serializer.is_valid(raise_exception=True)
        order_items = order_item_serializer.save()
        # Update the total price in the corresponding Order
        order = get_object_or_404(Order, id=pk)
        order.total = total_price
        order.save()
        # Delete cart items
        cart_items.delete()
        return Response({"detail": "Order items created successfully."}, status=status.HTTP_201_CREATED)
        #returns JSON response with 201 status code