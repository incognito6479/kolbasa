from django.urls import path
from rest_framework import routers

from .api_view import OrderViewSet, InvoiceViewSet, ReturnItemViewSet
from .views import OrderCreateView, OrderListView, OrderUpdateView, OrderDetailView, \
    OrderDeleteView, OrderActionView, ajax_print_invoice, download_invoice_excel, \
    InvoiceProviderCreateView, InvoiceProviderUpdateView, ReturnItemListView, ReturnItemAction, RetailOrderListView, \
    RetailOrderUpdateView, RetailOrderDetailView, RetailOrderActionView, RetailOrderCreateView

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'return_items', ReturnItemViewSet)

urlpatterns = [
    # path('order/order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order/order_list/', OrderListView.as_view(), name='order_list'),
    path('order/order_update/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('order/order_detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/order_delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('order/order_actions/<int:pk>/', OrderActionView.as_view(), name='order_actions'),

    path('retail_order/order_list/', RetailOrderListView.as_view(), name='retail_order_list'),
    path('retail_order/order_create/', RetailOrderCreateView.as_view(), name='retail_order_create'),
    path('retail_order/order_update/<int:pk>/', RetailOrderUpdateView.as_view(), name='retail_order_update'),
    path('retail_order/order_detail/<int:pk>/', RetailOrderDetailView.as_view(), name='retail_order_detail'),
    path('retail_order/order_actions/<int:pk>/', RetailOrderActionView.as_view(), name='retail_order_actions'),

    path('return_items/', ReturnItemListView.as_view(), name='return_items'),
    path('return_items/action/', ReturnItemAction.as_view(), name='return_items_action'),

    path('order/invoice_print_ajax', ajax_print_invoice, name="order_invoice_print_ajax"),
    path('order/invoice_excel_download/<int:pk>/', download_invoice_excel, name="invoice_excel_download"),

    path('order/order_invoice_provider_create/', InvoiceProviderCreateView.as_view(),
         name='order_invoice_provider_create'),
    path('order/order_invoice_provider_update/<int:pk>/', InvoiceProviderUpdateView.as_view(),
         name='order_invoice_provider_update'),
]
