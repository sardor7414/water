from rest_framework import serializers
from .models import CategoryCustomer, Customer, Order, DailyOrder, OldCustomer, OrderByDailyOrder
from rest_framework import status
import datetime
import requests


class CategoryCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryCustomer
        fields = ('id', 'name')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'area', 'phone', 'phone1')


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'driver', 'total_quantity', 'total_returned_products', 'created_at')

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")


class DailyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyOrder
        fields = '__all__'

    def validate(self, data):
        date = data.get('date')
        order_time = data.get('order_time')

        if order_time and not isinstance(order_time, datetime.datetime):
            raise serializers.ValidationError("order_time turini datetime bo'lishi kerak")

        if date and order_time and order_time.date() != date:
            raise serializers.ValidationError("order_time va date mos kelishi kerak")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = str(representation['date'])
        representation['order_time'] = str(representation['order_time'])
        return representation




class OldCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OldCustomer
        fields = '__all__'


class OrderByDailyOrderSerializer(serializers.ModelSerializer):
    total_debt_product_box = serializers.IntegerField(read_only=True)
    total_debt_customer = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrderByDailyOrder
        fields = '__all__'

    def calculate_debt(self, instance):
        customer_id = instance.daily_order.customer.id
        debt_url = f"https://sayqal.pythonanywhere.com/calculate-debt/{customer_id}/"
        try:
            response = requests.get(debt_url)
            if response.status_code == status.HTTP_200_OK:
                debt_data = response.json()
                print(debt_data)
                # data['total_debt_box'] = debt_data['total_debt_product_box']
                # data['total_debt_customer'] = debt_data['total_debt_customer']
                return debt_data
        except Exception as e:
            # Handle exceptions
            pass

    def to_representation(self, instance):
        res = super().to_representation(instance)
        debt_data = self.calculate_debt(instance)
        res['story_customer'] = debt_data
        return res


class CreateOrderByDailyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderByDailyOrder
        fields = '__all__'