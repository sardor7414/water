# Generated by Django 5.0.2 on 2024-03-14 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_orderbydailyorder_customer_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderbydailyorder',
            name='customer_name',
        ),
    ]
