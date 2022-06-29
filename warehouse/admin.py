from django.contrib import admin
from .models import Warehouse, WarehouseProduct


admin.site.register(Warehouse)
admin.site.register(WarehouseProduct)