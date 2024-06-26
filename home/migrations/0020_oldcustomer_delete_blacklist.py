# Generated by Django 5.0.2 on 2024-03-02 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_remove_blacklist_customer_blacklist_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('phone1', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('area', models.CharField(max_length=255)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('category', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Avvalgi Mijozlar',
            },
        ),
        migrations.DeleteModel(
            name='Blacklist',
        ),
    ]
