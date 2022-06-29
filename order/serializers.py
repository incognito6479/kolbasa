from rest_framework import serializers

from counter_party.api_view import CounterPartySerializer
from counter_party.models import CounterParty
from order.models import OrderItem, Order, InvoiceItem, ReturnItem, Invoice
from product.api_view import WarehouseProductSerializer
from user.models import Deliver
from user.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = 'id', 'warehouse_product_id', 'count', 'price', 'total'


class OrderSerializer(serializers.ModelSerializer):
    order_items_objs = OrderItemSerializer(many=True, read_only=False, source='order_items')

    class Meta:
        model = Order
        fields = 'id', 'created', 'user', 'counter_party', 'status', 'comment', 'total', 'order_items_objs'


class InvoiceItemSerializer(serializers.ModelSerializer):
    warehouse_product_id = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = 'id', 'order_item', 'warehouse_product_id', 'count', 'total_without_discount', 'total', 'item_type',

    @staticmethod
    def get_warehouse_product_id(obj):
        return obj.order_item.warehouse_product_id


class OrderSerializerForInvoice(serializers.ModelSerializer):
    order_items_objs = OrderItemSerializer(many=True, read_only=False, source='order_items')
    counter_party_obj = CounterPartySerializer(many=False, read_only=False, source='counter_party')

    class Meta:
        model = Order
        fields = 'id', 'created', 'user', 'counter_party_obj', 'status', 'total', 'order_items_objs'


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_item_obj = InvoiceItemSerializer(many=True, read_only=True, source='invoice_items')
    order_obj = OrderSerializerForInvoice(many=False, read_only=True, source='order')

    class Meta:
        model = Invoice
        fields = 'id', 'order_obj', 'user', 'status', \
                 'total', \
                 'invoice_item_obj', 'photo'


class DeliverSerializer(serializers.ModelSerializer):
    user_obj = UserSerializer(many=False, read_only=True, source='user')

    class Meta:
        model = Deliver
        fields = 'user_obj',


class ReturnItemSerializer(serializers.ModelSerializer):
    warehouse_product_obj = WarehouseProductSerializer(many=False, read_only=True, source='warehouse_product')

    class Meta:
        model = ReturnItem
        fields = 'count', 'price', 'total', 'warehouse_product_obj'


class CounterPartySerializerForReturnItem(CounterPartySerializer):
    return_items_objs = ReturnItemSerializer(many=True, read_only=True, source='return_items')

    class Meta:
        model = CounterParty
        fields = 'id', 'full_name', 'phone_number', 'address', 'landmark', \
                 'region', 'content', 'balance', 'marker', 'return_items_objs'