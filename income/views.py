from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, ListView
from django.views.generic import View

from payment.models import PaymentLog
from .models import Income, IncomeItem
from product.models import ProductCategory, Product
from .helpers import add_income_items, delete_income_item, change_income_status, income_payment
from warehouse.models import WarehouseProduct


class IncomeCreateView(CreateView):
    model = Income
    template_name = 'crm/income/income_create.html'
    fields = 'provider', 'warehouse'

    def get_context_data(self, **kwargs):
        context = super(IncomeCreateView, self).get_context_data()
        context['item_list'] = Income.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'created'
        form.instance.total = 0
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('income_detail', kwargs={'pk': self.object.pk})


class IncomeListView(ListView):
    model = Income
    template_name = 'crm/income/income_list.html'
    context_object_name = 'income'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')
        income = Income.objects.all()

        context['income'] = income
        context['end_date'] = end_date
        context['start_date'] = start_date
        context['status'] = status
        return context

    def get_queryset(self):
        income = super(IncomeListView, self).get_queryset()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        if start_date and end_date:
            income = Income.objects.filter(
                created__range=[
                    start_date,
                    end_date
                ]
            )
        if status:
            income = income.filter(
                status=status
            )
        else:
            income = income.exclude(status='rejected')

        return income


class IncomeUpdateView(UpdateView):
    model = Income
    fields = 'counter_party', 'status', 'warehouse'
    template_name = 'crm/income/income_update.html'
    success_url = reverse_lazy('income_list')

    def get_context_data(self, **kwargs):
        context = super(IncomeUpdateView, self).get_context_data()
        context['id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        income_instance = Income.objects.get(id=self.object.pk)
        income_items = IncomeItem.objects.filter(income=income_instance)
        if form.instance.status == 'completed':
            for income_item in income_items:
                obj, created = WarehouseProduct.objects.get_or_create(warehouse_id=income_instance.warehouse_id,
                                                                      product_id=income_item.product_id,
                                                                      defaults={
                                                                          'count': income_item.count,
                                                                          'self_price': income_item.price,
                                                                      }
                                                                      )
                if not created:
                    obj.count = income_item.count
                    obj.self_price = income_item.price
                    obj.save()
        if form.instance.status == 'rejected' and income_instance.status == 'completed':
            for income_item in income_items:
                warehouse_products = WarehouseProduct.objects.filter(warehouse_id=income_instance.warehouse_id,
                                                                     product_id=income_item.product_id)
                for warehouse_product in warehouse_products:
                    if income_item.product_id == warehouse_product.product_id:
                        warehouse_product.count -= income_item.count
                        warehouse_product.save()
        return super().form_valid(form)


class IncomeDetailView(TemplateView):
    template_name = 'crm/income/income_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        income = Income.objects.get(id=kwargs['pk'])
        context['income'] = income
        context['income_items'] = IncomeItem.objects.filter(income=income)
        context['product_categories'] = ProductCategory.objects.all()
        context['products'] = Product.objects.all()
        context['payments'] = PaymentLog.objects.filter(outcat='income', model_id=income.id)
        return context


class IncomeActionView(View):

    def post(self, request, pk):
        action = request.POST.get('action', None)
        print(self)
        actions = {
            'add_income_items': add_income_items,
            'change_income_status': change_income_status,
            'delete_income_item': delete_income_item,
            'income_payment': income_payment,
        }
        actions[action](request, self.kwargs)
        return redirect(reverse('income_detail', kwargs={'pk': self.kwargs['pk']}))
