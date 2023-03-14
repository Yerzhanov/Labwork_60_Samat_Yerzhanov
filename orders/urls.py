from django.urls import path
from orders.views import OrderCreateView, OrderListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name = 'orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order')

]
