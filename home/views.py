from django.db.models import Sum
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsSuperUser
from .serializers import (CategoryCustomerSerializer, CustomerSerializer, CustomerDataSerializer, OrderSerializer,
                          DailyOrderSerializer, OldCustomerSerializer, OrderByDailyOrderSerializer)
from .models import CategoryCustomer, Customer,LocalArea, DeliveryDriver, DailyOrder, Order, OrderByDailyOrder, OldCustomer, Product
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


# Create your views here.
class CategoryCustomerAPI(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser)

    def post(self, request):
        data = request.data
        serializer = CategoryCustomerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def get_queryset(self):
        return CategoryCustomer.objects.order_by('-id')

    def get(self, request):
        serializer = CategoryCustomerSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        category = CategoryCustomer.objects.filter(id=pk).first()
        serializer = CategoryCustomerSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class CustomerAPI(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        serializer = CustomerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def get_queryset(self):
        return Customer.objects.all()

    def get(self, request):
        params = request.query_params
        page = int(params.get('page', 1))
        offset = 5

        customers = self.get_queryset().order_by('-id')
        total_qty = customers.count()
        serializer = CustomerSerializer(customers[page * offset - offset: page * offset], many=True)
        return Response({
            "count": total_qty,
            "next": page + 1 if page * offset < total_qty else None,
            "back": page - 1 if page > 1 else None,
            "data": serializer.data
        })

    def patch(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        data = {}
        for field in request.data:
            if hasattr(customer, field):
                setattr(customer, field, request.data[field])
                data[field] = request.data[field]

        customer.save()
        return Response(data)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise HTTP_400_BAD_REQUEST


class CustomerDataAPI(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request, pk):
        customer = Customer.objects.filter(id=pk).first()
        if not customer:
            return Response({
                "message": "Bunday ID bilan mijoz topilmadi!"
            }, status=HTTP_204_NO_CONTENT)
        serializer = CustomerDataSerializer(customer)
        return Response(serializer.data)


class OrderAPI(APIView):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Order.objects.order_by('-id')

    def get(self, request):
        serializer = OrderSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        order = Order.objects.filter(id=pk).first()
        if order:
            data = {}
            for field in request.data:
                if hasattr(order, field):
                    if field == 'driver':
                        try:
                            driver_instance = DeliveryDriver.objects.get(id=request.data[field])
                            setattr(order, field, driver_instance)
                            data[field] = request.data[field]
                        except DeliveryDriver.DoesNotExist:
                            pass
                    else:
                        setattr(order, field, request.data[field])
                        data[field] = request.data[field]

            order.save()
            return Response(data)
        else:
            return Response({"error": "Bunday ID bilan yuk topilmadi"}, status=HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        order = self.get_queryset().filter(id=pk).first()
        if not order:
            return Response({"meesage": "Bunday ID bilan buyurtma topilmadi!"})
        order.delete()
        return Response({"message": "Buyurtma o'chirildi"}, status=HTTP_204_NO_CONTENT)


class DailyOrderAPI(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        daily_orders = DailyOrder.objects.all()
        serializer = DailyOrderSerializer(daily_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DailyOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            daily_order = DailyOrder.objects.get(pk=pk)
        except DailyOrder.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = DailyOrderSerializer(daily_order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            daily_order = DailyOrder.objects.get(pk=pk)
        except DailyOrder.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        daily_order.delete()
        return Response(status=HTTP_204_NO_CONTENT)




class GetDailyOrderDataAPI(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        daily_order = DailyOrder.objects.filter(id=pk).first()
        if not daily_order:
            return Response({"error": "Bunday ID bilan kunlik buyurtma topilmadi"}, status=HTTP_204_NO_CONTENT)
        serializer = DailyOrderSerializer(daily_order)
        return Response(serializer.data)




class OrderByDailyOrderList(APIView):
    def get(self, request, order_id):
        order_by_daily_orders = OrderByDailyOrder.objects.filter(order_id=order_id)
        if order_by_daily_orders.exists():  # Tekshirish
            serializer = OrderByDailyOrderSerializer(order_by_daily_orders, many=True)  # Faqat bitta obyektni olish
            return Response(serializer.data)
        else:
            return Response({"message": "Order not found"}, status=HTTP_404_NOT_FOUND)




class OrderByDailyOrderDetail(APIView):
    permission_classes = (IsAuthenticated, )
    def get_object(self, pk):
        return OrderByDailyOrder.objects.filter(order_id=pk).first()

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderByDailyOrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        # OrderByDailyOrder obyektini qidirish
        order_by_daily_order = OrderByDailyOrder.objects.filter(pk=pk).first()

        # Agar obyekt topilmasa 404 xatolik qaytariladi
        if not order_by_daily_order:
            return Response({"message": "OrderByDailyOrder not found"}, status=HTTP_404_NOT_FOUND)

        # Serializer yaratish
        serializer = OrderByDailyOrderSerializer(order_by_daily_order, data=request.data, partial=True)

        # Ma'lumotlarni validatsiya qilish
        if serializer.is_valid():
            # Ma'lumotlarni saqlash
            serializer.save()
            # Yangilangan ma'lumotni qaytarish
            return Response(serializer.data)
        else:
            # Agar ma'lumotlar to'g'ri kelmagan bo'lsa, xatolik qaytarish
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        return Response(status=HTTP_204_NO_CONTENT)



class CalculateDebtAPI(APIView):
    def get(self, request, customer_id):
        # Get all OrderByDailyOrder instances related to the given customer_id
        order_by_daily_orders = OrderByDailyOrder.objects.filter(daily_order__customer_id=customer_id)

        # Initialize variables to store debt calculations
        total_debt_product_box = 0
        total_debt_customer = 0

        # Iterate through each OrderByDailyOrder instance and calculate debts
        for order_by_daily_order in order_by_daily_orders:
            total_debt_product_box += order_by_daily_order.debt_product_box
            total_debt_customer += order_by_daily_order.debt_customer

        # Prepare response data
        response_data = {
            'total_debt_product_box': total_debt_product_box,
            'total_debt_customer': total_debt_customer
        }

        # Return the response
        return Response(response_data)


class UpdateDailyOrdersByOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get_daily_orders(self, order_id):
        return DailyOrder.objects.filter(order_id=order_id)

    def patch(self, request, order_id):
        # Get all DailyOrder instances related to the given order_id
        daily_orders = self.get_daily_orders(order_id)

        # Check if any instances exist
        if not daily_orders.exists():
            return Response({"message": "No DailyOrders found for the given order_id"}, status=HTTP_404_NOT_FOUND)

        # Serialize the request data
        serializer = DailyOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Iterate through each DailyOrder instance and update with new data
        for daily_order in daily_orders:
            serializer.update(daily_order, serializer.validated_data)

        return Response(serializer.data)




class DashboardAPI(APIView):
    def get(self, request):
        customer_count = Customer.objects.count()
        driver_count = DeliveryDriver.objects.count()
        product_count = Product.objects.count()
        category_customer_count = CategoryCustomer.objects.count()
        old_customer_count = OldCustomer.objects.count()
        debt_customers = OrderByDailyOrder.objects.filter(debt_customer__gt=0)
        debt_customer_count = debt_customers.count()
        total_amount_sum = debt_customers.aggregate(total_debt_customer_sum=Sum('debt_customer'))[
            'total_debt_customer_sum']

        data = {
            'customer_count': customer_count,
            'driver_count': driver_count,
            'product_count': product_count,
            'category_customer_count': category_customer_count,
            'old_customer_count': old_customer_count,
            'debt_customer_count': debt_customer_count,
            'total_debt_customer_sum': total_amount_sum
        }

        return Response(data)