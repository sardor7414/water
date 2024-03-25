from django.db import models
from django.utils import timezone

# Create your models here.

class DefaultAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(DefaultAbstract):
    name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    price = models.IntegerField(verbose_name="Narxi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Mahsulotlar"

class CategoryCustomer(DefaultAbstract):
    name = models.CharField(max_length=255, verbose_name="Mijoz toifasi: ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Mijoz kategoriyalari"

class LocalArea(DefaultAbstract):
    name = models.CharField(max_length=255, verbose_name="Mahalliy hudud", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Hudud"

class Customer(DefaultAbstract):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, unique=True)
    phone1 = models.CharField(max_length=13, unique=True, blank=True, null=True)
    area = models.ForeignKey(LocalArea, on_delete=models.CASCADE, verbose_name="Hudud (Mahalla, tuman)")
    latitude = models.FloatField(blank=True, null=True)  # Kenglik
    longitude = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(
        CategoryCustomer, on_delete=models.CASCADE, related_name='category_customer'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Mijozlar"


class DeliveryDriver(DefaultAbstract):
    name = models.CharField(max_length=255, verbose_name="Yukni yetkazib beruvchi haydovchi FIO")
    phone = models.CharField(max_length=13, unique=True, verbose_name="Telefon raqami")
    address = models.CharField(max_length=255, verbose_name="Haydovchi manzili")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Haydovchilar"


class Order(DefaultAbstract):
    driver = models.ForeignKey(DeliveryDriver, on_delete=models.SET_NULL, null=True, verbose_name="Haydovchi")
    total_quantity = models.IntegerField(verbose_name="Jami buyurtma soni")
    total_returned_products = models.IntegerField(verbose_name="Jami qaytarilgan mahsulotlar soni", blank=True, null=True)

    def __str__(self):
        return f"Buyurtma №: {self.id}"

    class Meta:
        verbose_name_plural = "Buyurtmalar"

class DailyOrder(DefaultAbstract):
    date = models.DateTimeField(verbose_name="Yetkazilish sanasi: ")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Mijoz: ")
    order_time = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma qilingan vaqti: ")
    quantity = models.IntegerField(verbose_name="buyurtma qilingan mahsulot soni: ")
    phone = models.CharField(max_length=13, blank=True, null=True)
    phone1 = models.CharField(max_length=13, blank=True, null=True)
    comment = models.CharField(max_length=255, verbose_name="Izoh")

    def auto_complate(self):
        if self.customer:
            self.customer_name = self.customer.name
            self.phone = self.customer.phone
            self.phone1 = self.customer.phone1
    def save(self, *args, **kwargs):
        self.auto_complate()
        super(DailyOrder, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer}: {self.date.strftime('%d-%m-%Y %H:%M')}"

    class Meta:
        verbose_name_plural = "Kunlik buyurtmalar"


class OrderByDailyOrder(DefaultAbstract):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Yuborilayotgan yuk: ")
    daily_order = models.ForeignKey(DailyOrder, on_delete=models.CASCADE, verbose_name="Kunlik buyurtmalar: ")
    customer_area = models.CharField(max_length=255, verbose_name="Mahalliy hudud", blank=True, null=True)
    customer_address = models.CharField(default="Manzil topilmadi", max_length=255, verbose_name="Buyurtma manzili: ")
    daily_order_quantity = models.IntegerField(default=0, verbose_name="Buyurtma qilingan mahsulot soni: ")
    product_price = models.IntegerField(default=15000,verbose_name="Mahsulot sotilgan narxi: ", blank=True, null=True)
    customer_phone = models.CharField(max_length=13)
    customer_phone1 = models.CharField(max_length=13, blank=True, null=True)
    received_quantity = models.IntegerField(default=0, verbose_name="Mijoz olgan mahsulot")
    ordered_product_box = models.IntegerField(default=0, verbose_name="Olingan mahsulotning qutisi soni")
    returned_product_box = models.IntegerField(default=0, verbose_name="Qaytarilgan mahsulot qutisi soni", blank=True, null=True)
    debt_product_box = models.IntegerField(default=0, verbose_name="Qarzdorlik: qutilardan", blank=True, null=True)
    total_amount = models.IntegerField(default=0, verbose_name="Jami buyurtma summasi", blank=True, null=True)
    paid_amount = models.IntegerField(default=0, verbose_name="Amalga oshirilgan to'lov", blank=True, null=True)
    debt_customer = models.IntegerField(default=0, verbose_name="Qarzdorlik")
    comments = models.TextField(blank=True, null=True, verbose_name="Izoh")

    def calculate_totals(self):
        self.ordered_product_box = self.received_quantity
        self.debt_product_box = self.ordered_product_box - self.returned_product_box
        if self.received_quantity and self.product_price:
            self.total_amount = self.received_quantity * self.product_price
        self.debt_customer = self.total_amount - self.paid_amount

    def save(self, *args, **kwargs):
        if self.daily_order and not self.pk:  # Agar yangi obyekt qo'shilgan bo'lsa
            self.customer_area = self.daily_order.customer.area.name
            self.customer_address = self.daily_order.customer.address
            self.daily_order_quantity = self.daily_order.quantity
            self.customer_phone = self.daily_order.phone
            self.customer_phone1 = self.daily_order.phone1
            self.comments = self.daily_order.comment
        self.calculate_totals()
        super(OrderByDailyOrder, self).save(*args, **kwargs)
        super(OrderByDailyOrder, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}->{self.daily_order}"

    class Meta:
        verbose_name_plural = "Tayyor buyurtmalar"



class OldCustomer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    phone1 = models.CharField(max_length=13, unique=True, blank=True, null=True)
    area = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)  # Kenglik
    longitude = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Qora Ro'yxat"



