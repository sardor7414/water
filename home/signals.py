from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Customer, OldCustomer, CategoryCustomer, LocalArea


# Post delete signal to move Customer to OldCustomer
@receiver(post_delete, sender=Customer)
def move_to_old_customer(sender, instance, **kwargs):
    OldCustomer.objects.create(
        id=instance.id, name=instance.name, address=instance.address, phone=instance.phone, phone1=instance.phone1,
        area=instance.area, latitude=instance.latitude, longitude=instance.longitude, category=instance.category
    )

@receiver(post_delete, sender=OldCustomer)
def move_to_customer(sender, instance, **kwargs):
    category = None
    if instance.category:
        # CategoryCustomer obyektini olish
        category, _ = CategoryCustomer.objects.get_or_create(name=instance.category)

    area = None
    if instance.area:
        # LocalArea obyektini olish
        area, _ = LocalArea.objects.get_or_create(name=instance.area)

    Customer.objects.create(
        name=instance.name,
        address=instance.address,
        phone=instance.phone,
        phone1=instance.phone1,
        area=area,
        latitude=instance.latitude,
        longitude=instance.longitude,
        category=category
    )
