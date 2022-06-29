import datetime

from django.core.files import File
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from counter_party.helpers import counter_party_balance_outcome
from counter_party.models import CounterParty
from order.filters import OrderFilter, InvoiceFilter, CounterPartyForReturnItemFilter
from order.models import Order, OrderItem, Invoice, ReturnItem
from order.serializers import OrderSerializer, InvoiceSerializer, \
    CounterPartySerializerForReturnItem
from product.api_view import CustomPagination
from user.models import Deliver, Agent
from warehouse.models import WarehouseProduct


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('order_items').all()
    serializer_class = OrderSerializer
    filter_class = OrderFilter
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )

    # {"user": 1,
    #  "counter_party": 1,
    # "order_items_objs":[
    #     {
    #         "warehouse_product": 1,
    #         "count": 10,
    #         "price": 123,
    #         "bonus_count": 1
    #     },
    #     {
    #         "warehouse_product": 2,
    #         "count": 10,
    #         "price": 123,
    #         "bonus_count": 1
    #     }
    # ]}

    def create(self, request, *args, **kwargs):
        order_serializer = self.get_serializer(data=request.data)
        agent = Agent.objects.get(user_id=request.data.get('user'))
        order = Order(user_id=request.data.get('user'),
                      agent_id=agent.id,
                      status='created',
                      total=0,
                      counter_party_id=request.data.get('counter_party'),
                      comment=request.data.get('comment'))
        order.save()
        order_items = request.data.pop('order_items_objs')
        warehouse_products = WarehouseProduct.objects.select_related('product') \
            .filter(id__in=(oi.get('warehouse_product')
                            for oi in order_items)).in_bulk()
        order_items_list = list()
        for order_item in order_items:
            wp = warehouse_products.get(order_item.get('warehouse_product'))
            count = float(order_item.get('count'))
            price = int(order_item.get('price'))
            total = int(count * price)
            order.total += total
            order_items_list.append(OrderItem(order=order,
                                              count=count,
                                              price=price,
                                              total=total,
                                              warehouse_product_id=wp.id))
            if float(order_item.get('bonus_count', 0)) > 0:
                order_items_list.append(OrderItem(order=order,
                                                  count=float(order_item.get('bonus_count')),
                                                  price=0,
                                                  total=0,
                                                  item_type=True,
                                                  warehouse_product_id=wp.id))
        OrderItem.objects.bulk_create(order_items_list)
        order.save()
        order_serializer.is_valid()
        headers = self.get_success_headers(order_serializer.data)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects \
        .prefetch_related('invoice_items',
                          'invoice_items__order_item',
                          'order__order_items') \
        .select_related('order', 'order__counter_party').all()
    serializer_class = InvoiceSerializer
    filter_class = InvoiceFilter
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )


class ReturnItemViewSet(viewsets.ModelViewSet):
    queryset = CounterParty.objects \
        .prefetch_related('return_items', 'return_items__warehouse_product',
                          'return_items__warehouse_product__warehouse',
                          'return_items__warehouse_product__product',
                          'return_items__warehouse_product__product__category') \
        .filter(return_items__isnull=False).distinct()
    serializer_class = CounterPartySerializerForReturnItem
    filter_class = CounterPartyForReturnItemFilter
    pagination_class = CustomPagination
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter
    )

    def create(self, request, *args, **kwargs):
        data = request.data.get('return_items')
        first_data = request.data.get('return_items')[0]
        deliver = Deliver.objects.get(user_id=first_data.get('user'))
        first_data['deliver'] = deliver.id
        first_data['total'] = 0
        first_data['price'] = 0
        return_item_serializer = self.get_serializer(data=first_data)
        return_items_list = list()
        for return_item_data in data:
            deliver = Deliver.objects.get(user_id=return_item_data.get('user'))
            return_item = ReturnItem(deliver=deliver,
                                     count=return_item_data.get('count'),
                                     counter_party_id=return_item_data.get('counter_party'),
                                     price=0,
                                     status='created',
                                     total=0,
                                     warehouse_product_id=return_item_data.get('warehouse_product'))
            return_items_list.append(return_item)
        ReturnItem.objects.bulk_create(return_items_list)
        return_item_serializer.is_valid()
        headers = self.get_success_headers(return_item_serializer.data)
        return Response(return_item_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ChangeInvoiceStatus(APIView):
    http_method_names = ['post']
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        invoice_pk = request.POST.get('invoice_id')
        invoice_status = request.POST.get('status')
        invoice_photo = request.FILES.get('invoice_photo')
        invoice_obj = Invoice.objects.get(pk=invoice_pk)
        order = invoice_obj.order
        if invoice_status == 'delivered':
            invoice_obj.photo.save(invoice_photo.name, File(invoice_photo))
            deliver_instance = invoice_obj.deliver
            deliver_instance.balance += invoice_obj.total * (deliver_instance.service_percent / 100)
            deliver_instance.save()
            agent_instance = order.agent
            agent_instance.balance += invoice_obj.total * (deliver_instance.service_percent / 100)
            agent_instance.save()
            counter_party_balance_outcome(invoice_obj.order.counter_party_id, invoice_obj.total)
            order.delivered_at = datetime.datetime.now()
        order.status = invoice_status
        invoice_obj.status = invoice_status
        invoice_obj.save()
        order.save()
        return Response(status=status.HTTP_200_OK, data={'invoice_pk': invoice_pk, 'action': 'status changed'})
