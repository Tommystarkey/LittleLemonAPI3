from django.db import models
from django.contrib.auth.models  import User
#django already comes with the user model
#and must be imported

 #db_index parameter is used to specify whether an index should be created on the database column
    #An index is a database feature that enhances the speed of data retrieval operations on a database table

class Category(models.Model):
    #the Category model allows you to define and store different categories in your application
    slug = models.SlugField()
    #SlugField is often used for storing a short label containing only letters,
    #numbers, underscores, or hyphens. It's typically used in URLs.
    title = models.CharField(max_length=255, db_index=True)
    #title field for category model



class MenuItem(models.Model):
#MenuItem model is designed to store information about individual items on a menu.
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # Establishes a many-to-one relationship between MenuItem and Category.
    # Each MenuItem is associated with a single Category.
    # If an attempt is made to delete a Category with associated menu items, a ProtectedError will be raised.



class Cart(models.Model):
#the Cart model is designed to store information about items added to a user's cart
#such as the user, the menu item, the quantity of the item, the unit price, and the total price
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    #user: A foreign key to the User model representing the user who owns the cart.
    #a User object is deleted, all related Cart objects with that user will also be delete
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    #menuitem: A foreign key to the MenuItem model representing the item added to the cart.
    #If a MenuItem object is deleted, all related Cart objects with that menu item will also be deleted.
    quantity = models.SmallIntegerField()
    #quantity: An integer field representing the quantity of the item in the cart.
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    #unit_price: A decimal field representing the unit price of the item.
    price = models.DecimalField(max_digits=6, decimal_places=2)
    #price: A decimal field representing the total price of the items with the specified quantity
 
    class Meta:
        unique_together = ('menuitem', 'user')
        # unique_together constraint ensures that there are no duplicate entries for the combination of menuitem and user, 
        # meaning a user cannot have the same menu item in their cart more than once.



class Order(models.Model):
#The Order model is designed to capture information about an order,
#including the user who placed the order, the assigned delivery crew, the order status, total cost, and the date of the order

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True, default=False) # 0 = false
    total = models.DecimalField(max_digits=6, decimal_places=2)
    #total field should have a default value or allow it to be nullable (null=True) unless you plan to set a value for it every time you create an order
    date = models.DateField(db_index=True)



class OrderItem(models.Model):
#The OrderItem model represents an individual item within an order made by a user, detailing the menu item, quantity, unit price, and total price.
   
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    #ForeignKey to the User model.Represents the user who placed the order.when the referenced User is deleted, also delete the associated OrderItem.
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    #ForeignKey to the MenuItem model. Represents the menu item included in the order.when the referenced MenuItem is deleted, also delete the associated OrderItem.
    quantity = models.SmallIntegerField()
    #Represents the quantity of the specified menu item in the order
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    #Represents the unit price of the menu item
    price = models.DecimalField(max_digits=6, decimal_places=2)
    #Represents the total price for the specified quantity of the menu item
   
    class Meta:
        unique_together = ('order', 'menuitem')
        #Specifies a unique constraint on the combination of the order and menuitem fields
        #each combination of a user and a menu item should be unique within the OrderItem model



