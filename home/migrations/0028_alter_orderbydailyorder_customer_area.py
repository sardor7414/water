# Generated by Django 5.0.2 on 2024-03-03 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_orderbydailyorder_customer_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbydailyorder',
            name='customer_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.localarea', verbose_name='Hudud (Tuman, Mahalla'),
        ),
    ]
