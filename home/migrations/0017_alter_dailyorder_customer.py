# Generated by Django 5.0.2 on 2024-03-02 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_remove_blacklist_customer_deleted_blacklist_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyorder',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.customer', verbose_name='Mijoz: '),
        ),
    ]