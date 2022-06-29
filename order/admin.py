from django.contrib import admin
from order.models import Order, Invoice, InvoiceItem, OrderItem, InvoiceProvider, ReturnItem

admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(OrderItem)
admin.site.register(InvoiceProvider)
admin.site.register(ReturnItem)
