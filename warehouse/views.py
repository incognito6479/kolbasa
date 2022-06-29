from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import Warehouse, WarehouseProduct


class WarehouseCreateView(CreateView):
    model = Warehouse
    fields = 'name', 'address'
    template_name = 'crm/warehouse/warehouse_create.html'

    def get_context_data(self, **kwargs):
        context = super(WarehouseCreateView, self).get_context_data()
        context['item_list'] = Warehouse.objects.all()
        return context

    def get_success_url(self):
        return self.request.path


class WarehouseUpdateView(UpdateView):
    model = Warehouse
    fields = 'name', 'address'
    template_name = 'crm/warehouse/warehouse_update.html'
    success_url = reverse_lazy('warehouse_create')

    def get_context_data(self, **kwargs):
        context = super(WarehouseUpdateView, self).get_context_data()
        context['id'] = self.kwargs['pk']
        return context


class WareHouseDelete(DeleteView):
    model = Warehouse
    success_url = reverse_lazy('warehouse_create')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class WarehouseDetailView(TemplateView):
    template_name = 'crm/warehouse/warehouse_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        warehouse_instance = Warehouse.objects.get(id=self.kwargs['pk'])
        warehouse_items = WarehouseProduct.objects.filter(warehouse_id=self.kwargs['pk'])
        context['warehouse'] = warehouse_instance
        context['warehouse_products'] = warehouse_items
        return context
