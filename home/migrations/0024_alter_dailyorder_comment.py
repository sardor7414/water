# Generated by Django 5.0.2 on 2024-03-03 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_dailyorder_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyorder',
            name='comment',
            field=models.CharField(default=1, max_length=255, verbose_name='Izoh'),
            preserve_default=False,
        ),
    ]