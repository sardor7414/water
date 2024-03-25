from django.urls import path
from .views import (CategoryCustomerAPI, CustomerAPI, CustomerDataAPI, OrderAPI, DailyOrderAPI, OrderByDailyOrderList,
                    GetDailyOrderDataAPI, CalculateDebtAPI, OrderByDailyOrderDetail, DashboardAPI)


urlpatterns = [
    path('dashboard/', DashboardAPI.as_view()),
    path('add-category/', CategoryCustomerAPI.as_view()),
    path('update-category/<int:pk>/', CategoryCustomerAPI.as_view()),
    path('add-customer/', CustomerAPI.as_view()),
    path('update-customer/<int:pk>/', CustomerAPI.as_view()),
    path('customer-data/<int:pk>/', CustomerDataAPI.as_view()),
    path('orders/', OrderAPI.as_view()),
    path('update-order/<int:pk>/', OrderAPI.as_view()),
    path('daily-order/', DailyOrderAPI.as_view()),
    path('update-daily-order/<int:pk>/', DailyOrderAPI.as_view()),
    path('get-daily-order-data/<int:pk>/', GetDailyOrderDataAPI.as_view()),
    path('get-order-by-daily-order/<int:order_id>/', OrderByDailyOrderList.as_view()),
    path('update-order-by-daily-order/<int:pk>/', OrderByDailyOrderDetail.as_view()),
    path('calculate-debt/<int:customer_id>/', CalculateDebtAPI.as_view())
]