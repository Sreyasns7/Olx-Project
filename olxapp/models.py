from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    user_type = models.CharField(default='1', max_length=10)
    user_type = models.CharField(default='2', max_length=10) 
    

class Usermembers(models.Model):
    user_member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)  # Add this line for image upload
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    from django.db import models



class ProductSubcategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    

class Product(models.Model):
    subcategory = models.ForeignKey('ProductSubcategory', on_delete=models.CASCADE)
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    approved = models.BooleanField(default=False)
    
    STATUS_CHOICES = (
        ('unsold', 'Unsold'),
        ('sold', 'Sold'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unsold')


    def __str__(self):
        return f"{self.subcategory.category.name} - {self.subcategory.name} - {self.name}"
    
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Add this line to track whether the message is read or not

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"


class Cart(models.Model):
    user_member = models.ForeignKey('Usermembers', on_delete=models.CASCADE, null=True)
    user_product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seller_name = models.CharField(max_length=255, blank=True, null=True) 



    def save(self, *args, **kwargs):
        # Calculate total_price before saving the Cart instance
        if self.user_product and self.user_product.price is not None:
            self.total_price = self.quantity * self.user_product.price
        else:
            self.total_price = 0

         # Fetch and store the seller's name from the associated product
        if self.user_product:
            self.seller_name = self.user_product.seller.username

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_member.user_member.username}'s Cart - {self.user_product.name}"
    
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Add a status field

class Order(models.Model):
    user_member = models.ForeignKey(Usermembers, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    card_number = models.CharField(max_length=16)
    shipping_address = models.TextField()
    cvv = models.CharField(max_length=4)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    seller_name = models.CharField(max_length=255, blank=True, null=True) 
    
   

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_confirmed:
            # Iterate over cart items and store seller name for each product
            seller_names = set(cart_item.user_product.seller.username for cart_item in self.cart.cart_items.all())
            if len(seller_names) == 1:
                self.seller_name = seller_names.pop()
                self.save(update_fields=['seller_name'])  # Save the updated seller_name

            # Mark associated products as sold
            for cart_item in self.cart.cart_items.all():
                cart_item.product.status = 'sold'
                cart_item.product.save()
        else:
            # Mark associated products as unsold
            for cart_item in self.cart.cart_items.all():
                cart_item.product.status = 'unsold'
                cart_item.product.save()



class Feedback(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"
    


    
