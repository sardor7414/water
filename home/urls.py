from django.urls import path
from .views import (CategoryCustomerAPI, CustomerAPI, CustomerDataAPI, OrderAPI, DailyOrderAPI, OrderByDailyOrderList,
                    GetDailyOrderDataAPI, CalculateDebtAPI, OrderByDailyOrderDetail, DashboardAPI, ReportDebtCustomerAPI,
                    OldCustomerReportAPI, HistoryCustomerAPI, CreateOrderByDailyOrder)


urlpatterns = [
    path('dashboard/', DashboardAPI.as_view()),
    path('report/', ReportDebtCustomerAPI.as_view()),
    path('report-old-customer/', OldCustomerReportAPI.as_view()),
    path('add-category/', CategoryCustomerAPI.as_view()),
    path('update-category/<int:pk>/', CategoryCustomerAPI.as_view()),
    path('add-customer/', CustomerAPI.as_view()),
    path('update-customer/<int:pk>/', CustomerAPI.as_view()),
    path('customer-data/<int:pk>/', CustomerDataAPI.as_view()),
    path('orders/', OrderAPI.as_view()),
    path('update-order/<int:pk>/', OrderAPI.as_view()),
    path('daily-order/', DailyOrderAPI.as_view()),
    path('update-daily-order/<int:pk>/', DailyOrderAPI.as_view()),
    path('create-order-by-daily-order/', CreateOrderByDailyOrder.as_view()),
    path('get-daily-order-data/<int:pk>/', GetDailyOrderDataAPI.as_view()),
    path('get-order-by-daily-order/<int:order_id>/', OrderByDailyOrderList.as_view()),
    path('update-order-by-daily-order/<int:pk>/', OrderByDailyOrderDetail.as_view()),
    path('calculate-debt/<int:customer_id>/', CalculateDebtAPI.as_view()),
    path('history-orders/<int:pk>/', HistoryCustomerAPI.as_view())
]