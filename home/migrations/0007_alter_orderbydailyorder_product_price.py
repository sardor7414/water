# Generated by Django 5.0.2 on 2024-02-29 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_orderbydailyorder_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbydailyorder',
            name='product_price',
            field=models.IntegerField(blank=True, default=15000, null=True, verbose_name='Mahsulot sotilgan narxi: '),
        ),
    ]
