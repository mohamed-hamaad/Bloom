from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.



# ANCHOR product
class Product(models.Model):
    # تعريف الاختيارات المتاحة في المتجر
    CATEGORY_CHOICES = [
        ('bouquets', 'Bouquets'),
        ('gifts', 'Gifts'),
        ('matching sets', 'Matching Sets'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # تحويل الحقل إلى ChoiceField عبر إضافة choices و default
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='bouquets'
    )
    
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name



# ANCHOR product image
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"

# ANCHOR order
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    isOrdered = models.BooleanField(default=False)
    def __str__(self):
        return f"Order #{self.id} - Total: {self.total_price}"

    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())

# ANCHOR order item
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    def __str__(self):
        return f"Order of {self.quantity} x {self.product.name}"
    
    def total_price(self):
        return self.quantity * self.product.price
