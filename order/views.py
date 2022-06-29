from django.db.models import F, Sum, Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, ListView
from django.views.generic import View
from django.http import JsonResponse
import json

from counter_party.models import RetailClient
from income.helpers import income_payment
from payment.models import PaymentLog
from user.models import Deliver
from warehouse.models import WarehouseProduct
from product.models import ProductCategory
from .helpers import add_order_item, change_order_status, delete_order_item, change_invoice_item_counts, \
    order_invoice_excel_download, return_items_acceptance, write_off_return_items, reject_return_items, \
    add_retail_order_item, change_retail_order_status, delete_retail_order_item, retail_order_payment
from .models import Order, OrderItem, Invoice, InvoiceItem, InvoiceProvider, ReturnItem, RetailOrder, RetailOrderItem


class InvoiceProviderCreateView(CreateView):
    model = InvoiceProvider
    fields = ('name', 'address', 'phone_number', 'logo')
    template_name = 'crm/invoice_provider/invoice_provider.html'
    success_url = reverse_lazy('order_invoice_provider_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice_providers'] = InvoiceProvider.objects.all()
        return context


class InvoiceProviderUpdateView(UpdateView):
    model = InvoiceProvider
    fields = ('name', 'address', 'phone_number', 'logo')
    template_name = 'crm/invoice_provider/invoice_provider_update.html'
    success_url = reverse_lazy('order_invoice_provider_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context


class OrderCreateView(CreateView):
    model = Order
    fields = ('counter_party',)
    template_name = 'crm/order/order_create.html'

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'created'
        return super().form_valid(form)


class OrderListView(ListView):
    model = Order
    template_name = 'crm/order/order_list.html'
    context_object_name = 'orders'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')
        context['status'] = status
        context['end_date'] = end_date
        context['start_date'] = start_date
        return context

    def get_queryset(self):
        orders = super(OrderListView, self).get_queryset()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        if start_date and end_date:
            orders = orders.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
        if status:
            orders = orders.filter(status=self.request.GET.get('status'))
        else:
            orders = orders.exclude(status='rejected')
        return orders


class OrderUpdateView(UpdateView):
    model = Order
    fields = ('counter_party',)
    template_name = 'crm/order/order_update.html'
    success_url = reverse_lazy('order_list')

    def get_form(self, form_class=None):
        return super(OrderUpdateView, self).get_form(form_class)


class OrderDetailView(TemplateView):
    template_name = 'crm/order/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data()
        order = Order.objects.get(id=self.kwargs['pk'])
        context['order'] = order
        context['order_items'] = OrderItem.objects.filter(order=order)
        context['order_items_totals'] = OrderItem.objects.filter(order=order) \
            .aggregate(total_count_p=Sum('count', filter=Q(warehouse_product__product__unit_type='piece')),
                       total=Sum('total'),
                       total_count_kg=Sum('count', filter=Q(warehouse_product__product__unit_type='kg')), )
        context['return_items'] = ReturnItem.objects.filter(counter_party_id=order.counter_party_id,
                                                            status='created')
        context['product_categories'] = ProductCategory.objects.all()
        context['warehouse_products'] = WarehouseProduct.objects.all()
        context['invoice_providers'] = InvoiceProvider.objects.all()
        context['invoice_delivers'] = Deliver.objects.all()
        if order.status == 'accepted' or order.status == 'completed' or order.status == 'delivered':
            context['invoice'] = Invoice.objects.get(order=order)
            context['invoice_items'] = InvoiceItem.objects \
                .select_related('order_item', 'order_item__warehouse_product',
                                'order_item__warehouse_product__product') \
                .filter(invoice__order=order)
        return context


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order_list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class OrderActionView(View):
    def post(self, request, pk):
        action = self.request.POST.get('action', None)
        actions = {
            'add_order_item': add_order_item,
            'change_order_status': change_order_status,
            'delete_order_item': delete_order_item,
            'change_invoice_item_counts': change_invoice_item_counts,
            'return_items_acceptance': return_items_acceptance,
        }
        actions[action](request, self.kwargs)
        return redirect(reverse_lazy('order_detail', kwargs={'pk': self.kwargs['pk']}))


class RetailOrderCreateView(CreateView):
    model = RetailOrder
    fields = ('client',)
    template_name = 'crm/order/retail_order_create.html'

    def get_success_url(self):
        return reverse_lazy('retail_order_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if not self.request.POST.get('client') and self.request.POST.get('full_name'):
            client = RetailClient(full_name=self.request.POST.get('full_name'),
                                  address=self.request.POST.get('address'),
                                  content=self.request.POST.get('content'),
                                  phone_number=self.request.POST.get('phone_number'))
            client.save()
            retail_order = RetailOrder.objects.create(user=self.request.user,
                                                      client=client,
                                                      status='created')
            return redirect(reverse_lazy('retail_order_detail', kwargs={'pk': retail_order.pk}))
        return super(RetailOrderCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        if not form.cleaned_data.get('client'):
            self.form_invalid(form)
        form.instance.user = self.request.user
        form.instance.status = 'created'
        return super().form_valid(form)


class RetailOrderListView(ListView):
    model = RetailOrder
    template_name = 'crm/order/retail_order_list.html'
    context_object_name = 'orders'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RetailOrderListView, self).get_context_data()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')
        context['status'] = status
        context['end_date'] = end_date
        context['start_date'] = start_date
        return context

    def get_queryset(self):
        orders = super(RetailOrderListView, self).get_queryset()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        if start_date and end_date:
            orders = orders.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
        if status:
            orders = orders.filter(status=self.request.GET.get('status'))
        else:
            orders = orders.exclude(status='rejected')
        return orders


class RetailOrderUpdateView(UpdateView):
    model = Order
    fields = ('client',)
    template_name = 'crm/order/retail_order_update.html'
    success_url = reverse_lazy('retail_order_list')

    def get_form(self, form_class=None):
        return super(RetailOrderUpdateView, self).get_form(form_class)


class RetailOrderDetailView(TemplateView):
    template_name = 'crm/order/retail_order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RetailOrderDetailView, self).get_context_data()
        order = RetailOrder.objects.get(id=self.kwargs['pk'])
        context['order'] = order
        context['order_items'] = RetailOrderItem.objects.filter(order=order)
        context['order_items_totals'] = RetailOrderItem.objects.filter(order=order) \
            .aggregate(total_count_p=Sum('count', filter=Q(warehouse_product__product__unit_type='piece')),
                       total=Sum('total'),
                       total_count_kg=Sum('count', filter=Q(warehouse_product__product__unit_type='kg')), )
        context['product_categories'] = ProductCategory.objects.all()
        context['warehouse_products'] = WarehouseProduct.objects.all()
        context['payments'] = PaymentLog.objects.filter(outcat='retail_order', model_id=order.id)
        return context


class RetailOrderActionView(View):
    def post(self, request, pk):
        action = self.request.POST.get('action', None)
        actions = {
            'add_retail_order_item': add_retail_order_item,
            'change_retail_order_status': change_retail_order_status,
            'delete_retail_order_item': delete_retail_order_item,
            'retail_order_payment': retail_order_payment,
        }
        actions[action](request, self.kwargs)
        return redirect(reverse_lazy('retail_order_detail', kwargs={'pk': self.kwargs['pk']}))


class ReturnItemAction(View):
    def post(self, request):
        action = self.request.POST.get('action', None)
        actions = {
            'write_off_return_items': write_off_return_items,
            'reject_return_items': reject_return_items,
        }
        actions[action](request, self.kwargs)
        return redirect(reverse_lazy('return_items'))


def ajax_print_invoice(request):
    data = json.loads(request.body)
    invoice = Invoice.objects.filter(id=int(data['id'])).select_related('order__counter_party', 'invoice_provider') \
        .values('id', 'created', 'total', 'discount', 'order__counter_party__full_name', 'order__counter_party__balance',
                'order__counter_party__phone_number', 'order__counter_party__address',
                'invoice_provider__name', 'invoice_provider__address', 'invoice_provider__phone_number',
                'invoice_provider__logo')
    invoice_items_simple = InvoiceItem.objects.filter(invoice_id=int(data['id']), item_type='simple').select_related(
        'order_item__warehouse_product__product') \
        .values('count', 'total', 'total_without_discount', 'order_item__warehouse_product__product__title',
                'order_item__warehouse_product__product__unit_type',
                'item_type',
                'order_item__price', 'order_item__warehouse_product__product__show_price')
    invoice_items_discount = InvoiceItem.objects.filter(invoice_id=int(data['id']), item_type='discount').select_related(
        'order_item__warehouse_product__product') \
        .values('count', 'total', 'total_without_discount', 'order_item__warehouse_product__product__title',
                'order_item__warehouse_product__product__unit_type',
                'item_type',
                'order_item__price', 'order_item__warehouse_product__product__show_price')
    invoice_items_bonus = InvoiceItem.objects.filter(invoice_id=int(data['id']), item_type='bonus').select_related(
        'order_item__warehouse_product__product') \
        .values('count', 'total', 'total_without_discount', 'order_item__warehouse_product__product__title',
                'order_item__warehouse_product__product__unit_type',
                'item_type',
                'order_item__price', 'order_item__warehouse_product__product__show_price')
    return JsonResponse({'data_0': list(invoice),
                         'data_1': list(invoice_items_simple),
                         'data_2': list(invoice_items_bonus),
                         'data_3': list(invoice_items_discount)})


def download_invoice_excel(request, pk):
    response = order_invoice_excel_download(pk)
    return response


class ReturnItemListView(ListView):
    model = ReturnItem
    template_name = 'crm/order/return_item_list.html'
    context_object_name = 'return_items'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReturnItemListView, self).get_context_data()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')
        context['status'] = status
        context['end_date'] = end_date
        context['start_date'] = start_date
        return context

    def get_queryset(self):
        return_items = super(ReturnItemListView, self).get_queryset()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status', '')
        return_items = return_items.order_by('-created')
        if start_date and end_date:
            return_items = return_items.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
        if status != '':
            return_items = return_items.filter(status=self.request.GET.get('status'))
        else:
            return_items = return_items.exclude(status='rejected')
        return return_items
