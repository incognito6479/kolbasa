from counter_party.helpers import counter_party_balance_income, counter_party_balance_outcome
from payment.helpers import payment_income_action, payment_outcome_action
from payment.models import Outlay
from .models import Income, IncomeItem
from django.db.models import Sum
from warehouse.models import WarehouseProduct


def add_income_items(request, kwargs):
    product_id = int(request.POST.get('product'))
    count = float(request.POST.get('count'))
    price = int(request.POST.get('price'))
    percent1 = float(request.POST.get('percent1'))
    percent2 = float(request.POST.get('percent2'))
    percent3 = float(request.POST.get('percent3'))
    percent4 = float(request.POST.get('percent4'))
    total = float("%.2f" % float(count * (price + price * ((percent1 + percent2 + percent3 + percent4) / 100))))
    obj, created = IncomeItem.objects.get_or_create(income_id=kwargs['pk'],
                                                    product_id=product_id,
                                                    defaults={
                                                        'count': count,
                                                        'price': price,
                                                        'percent1': percent1,
                                                        'percent2': percent2,
                                                        'percent3': percent3,
                                                        'percent4': percent4,
                                                        'total': total,
                                                    }
                                                    )
    if not created:
        obj.count = count
        obj.price = price
        obj.percent1 = percent1
        obj.percent2 = percent2
        obj.percent3 = percent3
        obj.percent4 = percent4
        obj.total = total
        obj.save()
    total_sum = IncomeItem.objects.filter(income_id=kwargs['pk']).aggregate(Sum('total'))
    Income.objects.filter(id=kwargs['pk']).update(total=total_sum.get('total__sum', 0))
    return 1


def change_income_status(request, kwargs):
    status = request.POST.get('change_status')
    income_instance = Income.objects.get(id=kwargs['pk'])
    income_items = IncomeItem.objects.filter(income_id=kwargs['pk'])
    if status == 'completed':
        for income_item in income_items:
            obj, created = WarehouseProduct.objects.get_or_create(warehouse_id=income_instance.warehouse_id,
                                                                  product_id=income_item.product_id,
                                                                  defaults={
                                                                      'count': income_item.count,
                                                                      'self_price': income_item.price,
                                                                  }
                                                                  )
            if not created:
                obj.count += income_item.count
                obj.self_price = ((obj.count * obj.self_price) +
                                  (income_item.count * income_item.price)) / (obj.count + income_item.count)
                obj.save()
        provider = income_instance.provider
        provider.balance += income_instance.total
        provider.save()
    if status == 'rejected' and income_instance.status == 'completed':
        for income_item in income_items:
            warehouse_products = WarehouseProduct.objects.filter(warehouse_id=income_instance.warehouse_id,
                                                                 product_id=income_item.product_id)
            for warehouse_product in warehouse_products:
                if income_item.product_id == warehouse_product.product_id:
                    warehouse_product.count -= income_item.count
                    warehouse_product.save()
        provider = income_instance.provider
        provider.balance += income_instance.total
        provider.save()
    Income.objects.filter(id=kwargs['pk']).update(status=status)
    return 1


def delete_income_item(request, kwargs):
    income_item_id = int(request.POST.get('income_item_id'))
    IncomeItem.objects.filter(id=income_item_id).delete()
    total_sum = IncomeItem.objects.filter(income_id=kwargs['pk']).aggregate(Sum('total'))
    if total_sum.get('total__sum'):
        Income.objects.filter(id=kwargs['pk']).update(total=total_sum.get('total__sum', 0))
    else:
        Income.objects.filter(id=kwargs['pk']).update(total=0)
    return 1


def income_payment(request, kwargs):
    income_id = int(request.POST.get('income_id', kwargs.get('pk')))
    income_instance = Income.objects.get(pk=income_id)
    payment_type = request.POST.get('payment_type')
    payment_method = request.POST.get('payment_method')
    amount = int(request.POST.get('amount'))
    outlay, created = Outlay.objects.get_or_create(outcat='income',
                                                   title='Выплата для погашения долга')
    if payment_type == 'income':
        payment_income_action('income', income_id, outlay, payment_method, amount, request.user)
        provider = income_instance.provider
        provider.balance += amount
        provider.save()
    elif payment_type == 'outcome':
        payment_outcome_action('income', income_id, outlay, payment_method, amount, request.user)
        provider = income_instance.provider
        provider.balance -= amount
        provider.save()
    return 1
