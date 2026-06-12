from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem
from django.core.exceptions import ValidationError


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Order)
admin.site.register(OrderItem)