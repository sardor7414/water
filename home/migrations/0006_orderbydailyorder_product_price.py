# Generated by Django 5.0.2 on 2024-02-29 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_orderbydailyorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbydailyorder',
            name='product_price',
            field=models.IntegerField(default=0, verbose_name='Mahsulot sotilgan narxi: '),
            preserve_default=False,
        ),
    ]
