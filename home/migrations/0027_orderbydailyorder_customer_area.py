# Generated by Django 5.0.2 on 2024-03-03 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_alter_dailyorder_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbydailyorder',
            name='customer_area',
            field=models.CharField(default=1, max_length=255, verbose_name='Hudud (Tuman, Mahalla)'),
            preserve_default=False,
        ),
    ]
