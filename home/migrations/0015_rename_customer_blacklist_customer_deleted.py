# Generated by Django 5.0.2 on 2024-03-02 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_blacklist_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blacklist',
            old_name='customer',
            new_name='customer_deleted',
        ),
    ]