from datetime import datetime

from django.db.models import Count, Q, Sum
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView
from django.urls import reverse_lazy

from counter_party.models import CounterParty, Provider, RetailClient
from order.models import Invoice, ReturnItem, RetailOrder
from payment.models import PaymentLog, Outlay
from counter_party.helpers import retail_client_report_excel_download, counter_party_report_excel_download


class CounterPartyView(CreateView):
    model = CounterParty
    fields = '__all__'
    template_name = 'crm/counter_party/counter_party.html'
    success_url = reverse_lazy('counter_party_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['counter_parties'] = CounterParty.objects.all()
        return context


class CounterPartyUpdateView(UpdateView):
    model = CounterParty
    fields = '__all__'
    template_name = 'crm/counter_party/counter_party_update.html'
    success_url = reverse_lazy('counter_party_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context


class CounterPartydeleteView(DeleteView):
    model = CounterParty
    success_url = reverse_lazy('counter_party_list')


class ProviderCreateView(CreateView):
    model = Provider
    fields = '__all__'
    template_name = 'crm/counter_party/provider_create.html'
    success_url = reverse_lazy('provider_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['providers'] = Provider.objects.all()
        return context


def counter_party_report_excel(request, pk):
    response = counter_party_report_excel_download(pk, request)
    return response


class CounterPartyReport(TemplateView):
    template_name = 'crm/counter_party/counter_party_report.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CounterPartyReport, self).get_context_data()

        counter_party = CounterParty.objects.get(pk=kwargs.get('pk'))
        context['counter_party'] = counter_party
        context['pk'] = kwargs.get('pk')

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        context['start_date'] = start_date
        context['end_date'] = end_date
        outlay, created = Outlay.objects.get_or_create(outcat='counter_party',
                                                       title='Выплата для погашения долга')
        payments = PaymentLog.objects.filter(outcat='counter_party',
                                             outlay=outlay,
                                             status='accepted',
                                             model_id=counter_party.id)
        # ('acceptance', 'Принятие'),
        # ('write-off', 'Списание'),

        if start_date and end_date:
            start_date += ' 00:00:00'
            end_date += ' 23:59:59'
            invoices = Invoice.objects.filter(order__counter_party=counter_party,
                                              status='delivered',
                                              created__range=[
                                                  start_date, end_date
                                              ])

            return_items = ReturnItem.objects.filter(counter_party=counter_party,
                                                     status__in=['acceptance', 'write-off'],
                                                     created__range=[
                                                         start_date, end_date
                                                     ])
            payments = payments.filter(
                created__range=[
                    start_date, end_date
                ])
        else:
            today_start = datetime.today().date().strftime('%Y-%m-%d') + ' 00:00:00'
            today_end = datetime.today().date().strftime('%Y-%m-%d') + ' 23:59:59'
            invoices = Invoice.objects.filter(order__counter_party=counter_party,
                                              status='delivered',
                                              created__range=[
                                                  today_start, today_end
                                              ])
            return_items = ReturnItem.objects.filter(counter_party=counter_party,
                                                     status__in=['acceptance', 'write-off'],
                                                     created__range=[
                                                         today_start, today_end
                                                     ])
            payments = payments.filter(
                created__range=[
                    today_start, today_end
                ])
        invoices_dicts = invoices.values('created', 'order_id', 'id', 'total', 'deliver__user__fullname')
        invoices_dicts = ((invoice_model['created'], {'title': 'Заказ №' + str(invoice_model['id'])
                                                               + ' ' + invoice_model['deliver__user__fullname'],
                                                      'created': invoice_model['created'],
                                                      'id': invoice_model['order_id'],
                                                      'type': 'invoice',
                                                      'type_display': 'Расход',
                                                      'amount': invoice_model['total']
                                                      }) for invoice_model in invoices_dicts)
        return_items_dicts = return_items.values('created', 'id', 'total', 'deliver__user__fullname')
        return_items_dicts = ((
            return_item_model['created'], {'title': 'Возврат №' + str(return_item_model['id'])
                                                    + ' ' + return_item_model[
                                                        'deliver__user__fullname'],
                                           'created': return_item_model['created'],
                                           'id': return_item_model['id'],
                                           'type': 'return_item',
                                           'type_display': 'Приход',
                                           'amount': return_item_model['total']}
        ) for return_item_model in return_items_dicts)
        payments_dicts = payments.values('created', 'id', 'amount', 'user__fullname')
        payments_dicts = ((
            payments_model['created'], {'title': 'Оплата №' + str(payments_model['id'])
                                                 + ' ' + payments_model[
                                                     'user__fullname'],
                                        'created': payments_model['created'],
                                        'id': payments_model['id'],
                                        'type': 'payment',
                                        'type_display': 'Приход',
                                        'amount': payments_model['amount']}
        ) for payments_model in payments_dicts)
        report_dict = list(invoices_dicts) + list(return_items_dicts) + list(payments_dicts)
        report_dict.sort()
        report_dict = {created: model for created, model in report_dict}
        context['reports'] = report_dict.values()
        return context


def retail_client_report_excel(request, pk):
    response = retail_client_report_excel_download(pk, request)
    return response


class RetailClientReport(TemplateView):
    template_name = 'crm/counter_party/retail_client_report.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RetailClientReport, self).get_context_data()
        context['pk'] = kwargs.get('pk')
        print(kwargs.get('pk'))
        retail_client = RetailClient.objects.get(pk=kwargs.get('pk'))
        context['retail_client'] = retail_client

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        context['start_date'] = start_date
        context['end_date'] = end_date
        payments = PaymentLog.objects.filter(outcat='retail_order',
                                             status='accepted')
        # ('acceptance', 'Принятие'),
        # ('write-off', 'Списание'),

        if start_date and end_date:
            start_date += ' 00:00:00'
            end_date += ' 23:59:59'
            retail_orders = RetailOrder.objects.filter(client=retail_client,
                                                       status='completed',
                                                       created__range=[
                                                           start_date, end_date
                                                       ])
            payments = payments.filter(
                model_id__in=retail_orders.values_list('id', flat=True)
            )
        else:
            today_start = datetime.today().date().strftime('%Y-%m-%d') + ' 00:00:00'
            today_end = datetime.today().date().strftime('%Y-%m-%d') + ' 23:59:59'
            retail_orders = RetailOrder.objects.filter(client=retail_client,
                                                       status='completed',
                                                       created__range=[
                                                           today_start, today_end
                                                       ])
            payments = payments.filter(
                model_id__in=retail_orders.values_list('id', flat=True)
            )
        retail_orders_dicts = retail_orders.values('created', 'id', 'total', 'user__username')
        retail_orders_dicts = ((retail_order['created'], {'title': 'Заказ №' + str(retail_order['id'])
                                                              + ' ' + retail_order['user__username'],
                                                     'created': retail_order['created'],
                                                     'id': retail_order['id'],
                                                     'type': 'retail_order',
                                                     'type_display': 'Расход',
                                                     'amount': retail_order['total']
                                                     }) for retail_order in retail_orders_dicts)
        payments_dicts = payments.values('created', 'id', 'amount', 'user__fullname')
        payments_dicts = ((
            payments_model['created'], {'title': 'Оплата №' + str(payments_model['id'])
                                                 + ' ' + payments_model[
                                                     'user__fullname'],
                                        'created': payments_model['created'],
                                        'id': payments_model['id'],
                                        'type': 'payment',
                                        'type_display': 'Приход',
                                        'amount': payments_model['amount']}
        ) for payments_model in payments_dicts)
        report_dict = list(retail_orders_dicts) + list(payments_dicts)
        report_dict.sort()
        report_dict = {created: model for created, model in report_dict}
        context['reports'] = report_dict.values()
        return context


class ProviderUpdateView(UpdateView):
    model = Provider
    fields = '__all__'
    template_name = 'crm/counter_party/provider_update.html'
    success_url = reverse_lazy('provider_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context


class ProviderDeleteView(DeleteView):
    model = Provider
    success_url = reverse_lazy('provider_create')


class RetailClientCreateView(CreateView):
    model = RetailClient
    fields = '__all__'
    template_name = 'crm/counter_party/retail_client_create.html'

    def get_success_url(self):
        return reverse_lazy('retail_client_list')


class RetailClientListView(ListView):
    model = RetailClient
    queryset = RetailClient.objects.annotate(
        retail_orders_count=Count('retail_orders',
                                  filter=Q(retail_orders__status__in=['created', 'completed']))
    ).all()
    template_name = 'crm/counter_party/retail_client_list.html'
    context_object_name = 'clients'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RetailClientListView, self).get_context_data()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')
        context['status'] = status
        context['end_date'] = end_date
        context['start_date'] = start_date
        return context

    def get_queryset(self):
        client = super(RetailClientListView, self).get_queryset()
        client = client.annotate(
            retail_orders_count=Count('retail_orders',
                                      filter=Q(retail_orders__status__in=['created', 'completed']))
        )
        #
        # start_date = self.request.GET.get('start_date')
        # end_date = self.request.GET.get('end_date')
        # status = self.request.GET.get('status')
        #
        # if start_date and end_date:
        #     client = client.filter(
        #         created__range=[
        #             start_date,
        #             end_date,
        #         ]
        #     )
        # if status:
        #     client = client.filter(status=self.request.GET.get('status'))
        # else:
        #     client = client.exclude(status='rejected')
        return client


class RetailClientUpdateView(UpdateView):
    model = RetailClient
    fields = '__all__'
    template_name = 'crm/counter_party/retail_client_update.html'
    success_url = reverse_lazy('retail_client_list')

    def get_form(self, form_class=None):
        return super(RetailClientUpdateView, self).get_form(form_class)


class RetailClientDetailView(TemplateView):
    template_name = 'crm/counter_party/retail_client_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RetailClientDetailView, self).get_context_data()
        client = RetailClient.objects.get(id=self.kwargs['pk'])
        context['order'] = client
        return client


class RetailClientDeleteView(DeleteView):
    model = RetailClient
    success_url = reverse_lazy('retail_client_list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

# class RetailOrderActionView(View):
#     def post(self, request, pk):
#         action = self.request.POST.get('action', None)
#         actions = {
#             'add_order_item': add_order_item,
#             'change_order_status': change_order_status,
#             'delete_order_item': delete_order_item,
#             'change_invoice_item_counts': change_invoice_item_counts,
#             'return_items_acceptance': return_items_acceptance,
#         }
#         actions[action](request, self.kwargs)
#         return redirect(reverse_lazy('retail_order_detail', kwargs={'pk': self.kwargs['pk']}))
