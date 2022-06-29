from django.shortcuts import redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import TemplateView, View
from .models import Movement, MovementItem
from django.urls import reverse_lazy
from warehouse.models import Warehouse, WarehouseProduct
from .helpers import add_movement_item, change_movement_status, delete_movement_item


class MovementCreateView(CreateView):
	model = Movement
	fields = 'from_warehouse', 'to_warehouse'
	template_name = 'crm/movement/movement_create.html'

	def get_context_data(self):
		context = super().get_context_data()
		context['item_list'] = Movement.objects.all()
		return context

	def get_success_url(self):
		return reverse_lazy('movement_detail', kwargs={'pk': self.object.pk})

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class MovementListView(ListView):
	model = Movement
	template_name = 'crm/movement/movement_list.html'
	context_object_name = 'movements'
	paginate_by = 25

	def get_context_data(self, **kwargs):
		context = super(MovementListView, self).get_context_data()
		movements = Movement.objects.all()
		start_date = self.request.GET.get('start_date')
		end_date = self.request.GET.get('end_date')
		status = self.request.GET.get('status')
		if status:
			movements = movements.filter(status=status)
		if start_date and end_date:
			movements = movements.filter(created__range=[
									start_date,
									end_date
								])
		context['movements'] = movements
		context['start_date'] = start_date
		context['end_date'] = end_date
		context['status'] = status
		return context


class MovementDetailView(TemplateView):
	template_name = 'crm/movement/movement_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		movement = Movement.objects.get(id=self.kwargs['pk'])
		warehouse = Warehouse.objects.get(id=movement.from_warehouse.id)
		context['movement'] = movement
		context['movement_item'] = MovementItem.objects.filter(movement_id=self.kwargs['pk'])
		context['warehouse'] = warehouse
		context['warehouse_products'] = WarehouseProduct.objects.filter(warehouse_id=warehouse.id)
		return context


class MovementUpdateView(UpdateView):
	model = Movement
	fields = 'from_warehouse', 'to_warehouse', 'status'
	success_url = reverse_lazy('movement_list')
	template_name = 'crm/movement/movement_update.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['id'] = self.kwargs['pk']
		return context


class MovementActionsView(View):
	def post(self, request, pk):
		action = request.POST.get('action', None)
		actions = {
			'add_movement_item': add_movement_item,
			'change_movement_status': change_movement_status,
			'delete_movement_item': delete_movement_item,
		}
		response = actions[action](request, self.kwargs)
		return redirect(reverse_lazy('movement_detail', kwargs={'pk': self.kwargs['pk']}))
