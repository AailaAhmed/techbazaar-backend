from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural="categories"
        ordering=["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    thumbnail = models.URLField(max_length=500,blank=True)
    is_active = models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):

    STATUS_CHOICES = [("processing","Processing"),
                      ("shipped","Shipped"),
                      ("delivered","Delivered"),
                      ("cancelled","Cancelled"),]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,null=True,blank=True,related_name='orders',)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country= models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="processing")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="items" )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

