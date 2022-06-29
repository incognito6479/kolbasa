from datetime import datetime

from django.db.models import Subquery, OuterRef, Sum, F
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView

from counter_party.models import CounterParty
from income.models import Income
from order.models import RetailOrder, Order, ReturnItem
from payment.helpers import payment_accept, payment_reject, payment_theory_excel, payment_real_excel
from payment.models import PaymentLog


class PaymentTreatment(TemplateView):
    template_name = 'crm/payment/payment_treatment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentTreatment, self).get_context_data(**kwargs)
        context['payments'] = PaymentLog.objects. \
            select_related('user').annotate(
            counter_party_name=Subquery(CounterParty.objects
                                        .filter(id=OuterRef('model_id'))
                                        .values_list('full_name'))
        ) \
            .filter(status='created')
        return context


class PaymentLogListView(ListView):
    model = PaymentLog
    template_name = 'crm/payment/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PaymentLogListView, self).get_context_data()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')

        context['status'] = status
        context['end_date'] = end_date
        context['start_date'] = start_date
        return context

    def get_queryset(self):
        payments = super(PaymentLogListView, self).get_queryset()

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        status = self.request.GET.get('status')
        payments = payments.annotate(
            counter_party_name=Subquery(CounterParty.objects
                                        .filter(id=OuterRef('model_id'))
                                        .values_list('full_name'))
        )

        if start_date and end_date:
            payments = payments.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
        if status:
            payments = payments.filter(status=self.request.GET.get('status'))
        else:
            payments.exclude(status='rejected')
        return payments


class PaymentAction(ListView):

    def post(self, request):
        action = self.request.POST.get('action', None)
        actions = {
            'payment_accept': payment_accept,
            'payment_reject': payment_reject,
        }
        actions[action](request, self.kwargs)
        return redirect(reverse('payment_treatment'))


def payment_real_excel_download(request):
    response = payment_real_excel(request)
    return response


class PaymentIncomeReal(TemplateView):
    model = PaymentLog
    template_name = 'crm/payment/payment_real_report.html'
    context_object_name = 'payments'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PaymentIncomeReal, self).get_context_data()
        payments_income = PaymentLog.objects.filter(status='accepted', payment_type='income')
        payments_outcome = PaymentLog.objects.filter(status='accepted', payment_type='outcome')

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        payments_income = payments_income.annotate(
            counter_party_name=Subquery(CounterParty.objects
                                        .filter(id=OuterRef('model_id'))
                                        .values_list('full_name'))
        )
        payments_outcome = payments_outcome.annotate(
            counter_party_name=Subquery(CounterParty.objects
                                        .filter(id=OuterRef('model_id'))
                                        .values_list('full_name'))
        )
        context['end_date'] = end_date
        context['start_date'] = start_date

        if start_date and end_date:
            start_date += ' 00:00:00'
            end_date += ' 23:59:59'
            payments_income = payments_income.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
            payments_outcome = payments_outcome.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
        else:
            today_start = datetime.today().date().strftime('%Y-%m-%d') + ' 00:00:00'
            today_end = datetime.today().date().strftime('%Y-%m-%d') + ' 23:59:59'
            payments_income = payments_income.filter(
                created__range=[
                    today_start,
                    today_end,
                ]
            )
            payments_outcome = payments_outcome.filter(
                created__range=[
                    today_start,
                    today_end,
                ]
            )

        context['payments_outcome'] = payments_outcome
        context['payments_outcome_total'] = payments_outcome.aggregate(total=Sum('amount'))
        context['payments_income'] = payments_income
        context['payments_income_total'] = payments_income.aggregate(total=Sum('amount'))

        return context


def payment_theory_report_excel(request):
    response = payment_theory_excel(request)
    return response


class PaymentIncomeTheory(TemplateView):
    model = PaymentLog
    template_name = 'crm/payment/payment_theory_report.html'
    context_object_name = 'payments'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PaymentIncomeTheory, self).get_context_data()
        retail_orders = RetailOrder.objects.filter(status='completed')
        orders = Order.objects.filter(status__in=['delivered',
                                                  'completed'])

        incomes = Income.objects.filter(status='completed')
        return_items = ReturnItem.objects.filter(status='write-off')

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        context['end_date'] = end_date
        context['start_date'] = start_date

        if start_date and end_date:
            start_date += ' 00:00:00'
            end_date += ' 23:59:59'
            retail_orders = retail_orders.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
            orders = orders.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
            incomes = incomes.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
            return_items = return_items.filter(
                created__range=[
                    start_date,
                    end_date,
                ]
            )
        else:
            today_start = datetime.today().date().strftime('%Y-%m-%d') + ' 00:00:00'
            today_end = datetime.today().date().strftime('%Y-%m-%d') + ' 23:59:59'
            retail_orders = retail_orders.filter(
                created__range=[
                    today_start,
                    today_end,
                ]
            )
            orders = orders.filter(
                created__range=[
                    today_start,
                    today_end,
                ]
            )
            incomes = incomes.filter(
                created__range=[
                    today_start,
                    today_end,
                ]
            )
            return_items = return_items.filter(
                created__range=[
                    today_start,
                    today_end,
                ]
            )

        orders = orders.annotate(
            deliver_percent=F('invoice__total') * (F('invoice__deliver__service_percent') / 100),
            agent_percent=F('invoice__total') * (F('agent__service_percent') / 100),
            self_price=Sum(F('order_items__warehouse_product__self_price') * F('order_items__count')),
            profit_amount=F('invoice__total') - F('self_price') - F('deliver_percent') - F('agent_percent'),
        )

        context['retail_orders'] = retail_orders
        context['orders'] = orders
        context['incomes'] = incomes
        context['return_items'] = return_items

        context['retail_orders_total'] = retail_orders.aggregate(total=Sum('total'))
        context['orders_total'] = orders.aggregate(total=Sum('profit_amount'))
        context['incomes_total'] = incomes.aggregate(total=Sum('total'))
        context['return_items_total'] = return_items.aggregate(total=Sum('total'))
        return context
