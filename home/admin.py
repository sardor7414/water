from django.contrib import admin
from .models import (Product, CategoryCustomer, LocalArea, Customer, DeliveryDriver, Order, DailyOrder, OrderByDailyOrder, OldCustomer)


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


@admin.register(CategoryCustomer)
class CategoryCustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')


@admin.register(LocalArea)
class LocalAreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'address', 'phone', 'phone1', 'area', 'latitude', 'longitude', 'category', 'created_at'
    )
    list_display_links = ('name', )
    list_filter = ('address', 'category', 'area', 'created_at')


@admin.register(DeliveryDriver)
class DeliveryDriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'address')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'total_quantity', 'total_returned_products')


@admin.register(DailyOrder)
class DailyOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'customer', 'order_time', 'quantity', 'phone', 'phone1', 'comment')


@admin.register(OrderByDailyOrder)
class OrderByDailyOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order', 'daily_order', 'customer_area', 'customer_address', 'daily_order_quantity', 'product_price', 'customer_phone',
        'customer_phone1', 'received_quantity', 'ordered_product_box', 'returned_product_box', 'debt_product_box',
        'total_amount', 'paid_amount', 'debt_customer', 'comments'
    )
    list_filter = ('id', 'order', 'daily_order', 'customer_area')

@admin.register(OldCustomer)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone', 'phone1', 'area', 'category')