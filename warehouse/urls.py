from django.urls import path
from .views import WarehouseCreateView, WarehouseUpdateView, WareHouseDelete, WarehouseDetailView


urlpatterns = [
    path('warehouse_create/', WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouse_update/<int:pk>', WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouse_delete/<int:pk>', WareHouseDelete.as_view(), name='warehouse_delete'),
    path('warehouse_detail/<int:pk>', WarehouseDetailView.as_view(), name='warehouse_detail'),
]
